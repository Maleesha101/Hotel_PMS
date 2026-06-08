import { prisma } from '../../config/prisma';
import { redis } from '../../config/redis';
import { env } from '../../config/env';
import bcrypt from 'bcryptjs';
import crypto from 'crypto';
import { signAccessToken, signRefreshToken, verifyRefreshToken, TokenPayload } from '../../shared/jwt';
import { UnauthorizedError, ConflictError, ForbiddenError, NotFoundError } from '../../shared/errors';
import { AuditAction } from '../../shared/enums';
import { AuditLogCreateDto } from '../audit/audit.types';
import { LoginResponse, TokenPair, RequestMeta } from './auth.types';
import { logger } from '../../config/logger';

export class AuthService {
  private async logAudit(data: AuditLogCreateDto) {
    await prisma.auditLog.create({ data });
  }

  // Helper to hash refresh token
  private hashRefreshToken(token: string): string {
    return crypto.createHash('sha256').update(token).digest('hex');
  }

  async login(email: string, password: string, meta: RequestMeta): Promise<LoginResponse> {
    const user = await prisma.user.findUnique({ where: { email } });
    if (!user) {
      await this.logAudit({ action: AuditAction.LOGIN_FAILED, ipAddress: meta.ipAddress, userAgent: meta.userAgent, details: { email } });
      throw new UnauthorizedError('Invalid credentials');
    }
    if (user.status !== 'ACTIVE') {
      await this.logAudit({ action: AuditAction.LOGIN_FAILED, userId: user.id, ipAddress: meta.ipAddress, userAgent: meta.userAgent, details: { reason: 'inactive' } });
      throw new UnauthorizedError('Account is inactive or suspended');
    }
    const passwordMatch = await bcrypt.compare(password, user.passwordHash);
    if (!passwordMatch) {
      await this.logAudit({ action: AuditAction.LOGIN_FAILED, userId: user.id, ipAddress: meta.ipAddress, userAgent: meta.userAgent });
      throw new UnauthorizedError('Invalid credentials');
    }
    // Issue tokens
    const accessToken = signAccessToken({ sub: user.id, email: user.email, role: user.role as any, name: user.name });
    const refreshToken = signRefreshToken(user.id);
    const tokenHash = this.hashRefreshToken(refreshToken);
    await prisma.refreshToken.create({
      data: {
        userId: user.id,
        tokenHash,
        deviceInfo: meta.deviceInfo,
        ipAddress: meta.ipAddress,
        expiresAt: new Date(Date.now() + this.parseExpiry(env.JWT_REFRESH_EXPIRY)),
      },
    });
    // Update login stats
    await prisma.user.update({
      where: { id: user.id },
      data: { lastLoginAt: new Date(), loginCount: { increment: 1 } },
    });
    await this.logAudit({ userId: user.id, action: AuditAction.LOGIN, ipAddress: meta.ipAddress, userAgent: meta.userAgent });
    return {
      accessToken,
      refreshToken,
      user: { id: user.id, name: user.name, email: user.email, role: user.role },
    };
  }

  // Helper to parse JWT expiry strings like '7d' or '15m'
  private parseExpiry(expiry: string): number {
    const match = expiry.match(/^(\d+)([smhd])$/);
    if (!match) return 0;
    const value = parseInt(match[1]);
    const unit = match[2];
    const msMap: Record<string, number> = { s: 1000, m: 60000, h: 3600000, d: 86400000 };
    return value * msMap[unit];
  }

  async logout(accessToken: string, userId: string): Promise<void> {
    // Decode token (ignore expiration errors)
    let payload: TokenPayload | null = null;
    try {
      payload = verifyAccessToken(accessToken);
    } catch (e) {
      // ignore verification errors, attempt to decode unsafe
      payload = null;
    }
    // Blocklist access token
    const now = Math.floor(Date.now() / 1000);
    let ttl = 1;
    if (payload && payload.exp) {
      ttl = Math.max(payload.exp - now, 1);
    }
    await redis.set(`blocklist:${accessToken}`, 'revoked', 'EX', ttl);
    // Revoke all non‑expired refresh tokens for user
    await prisma.refreshToken.updateMany({
      where: { userId, expiresAt: { gt: new Date() }, revokedAt: null },
      data: { revokedAt: new Date() },
    });
    await this.logAudit({ userId, action: AuditAction.LOGOUT });
  }

  async refreshTokens(rawRefreshToken: string, meta: RequestMeta): Promise<TokenPair> {
    const payload = verifyRefreshToken(rawRefreshToken);
    const userId = payload.sub;
    const tokenHash = this.hashRefreshToken(rawRefreshToken);
    const existing = await prisma.refreshToken.findFirst({
      where: { tokenHash, revokedAt: null, expiresAt: { gt: new Date() } },
    });
    if (!existing) {
      // reuse or invalid token – revoke all tokens for user
      await prisma.refreshToken.updateMany({ where: { userId }, data: { revokedAt: new Date() } });
      await this.logAudit({ userId, action: AuditAction.TOKEN_REVOKED, details: { reason: 'reuse_detected' } });
      throw new UnauthorizedError('Invalid refresh token');
    }
    // Rotate token
    await prisma.refreshToken.update({ where: { id: existing.id }, data: { revokedAt: new Date() } });
    const userRecord = await prisma.user.findUnique({ where: { id: userId } });
    if (!userRecord) throw new NotFoundError('User not found');
    const newAccess = signAccessToken({ sub: userId, email: userRecord.email, role: userRecord.role as any, name: userRecord.name });
    const newRefresh = signRefreshToken(userId);
    const newHash = this.hashRefreshToken(newRefresh);
    await prisma.refreshToken.create({
      data: {
        userId,
        tokenHash: newHash,
        deviceInfo: meta.deviceInfo,
        ipAddress: meta.ipAddress,
        expiresAt: new Date(Date.now() + this.parseExpiry(env.JWT_REFRESH_EXPIRY)),
      },
    });
    await this.logAudit({ userId, action: AuditAction.TOKEN_REFRESHED, ipAddress: meta.ipAddress, userAgent: meta.userAgent });
    return { accessToken: newAccess, refreshToken: newRefresh };
  }

  async verifyToken(token: string): Promise<TokenPayload> {
    return verifyAccessToken(token);
  }

  async changePassword(userId: string, currentPassword: string, newPassword: string): Promise<void> {
    const user = await prisma.user.findUnique({ where: { id: userId } });
    if (!user) throw new NotFoundError('User not found');
    const match = await bcrypt.compare(currentPassword, user.passwordHash);
    if (!match) throw new UnauthorizedError('Current password is incorrect');
    const newHash = await bcrypt.hash(newPassword, env.BCRYPT_ROUNDS);
    await prisma.user.update({ where: { id: userId }, data: { passwordHash: newHash } });
    await this.logAudit({ userId, action: AuditAction.PASSWORD_CHANGED });
  }

  async revokeAllSessions(userId: string): Promise<void> {
    // Revoke all refresh tokens
    await prisma.refreshToken.updateMany({ where: { userId }, data: { revokedAt: new Date() } });
    // Optionally, we could blocklist all access tokens if we stored jti, but here we rely on blocklist per logout
    await this.logAudit({ userId, action: AuditAction.TOKEN_REVOKED, details: { reason: 'revoke_all' } });
  }

  async adminResetPassword(targetUserId: string, adminId: string): Promise<{ temporaryPassword: string }> {
    const tempPassword = crypto.randomBytes(8).toString('base64'); // 12‑char base64
    const hash = await bcrypt.hash(tempPassword, env.BCRYPT_ROUNDS);
    await prisma.user.update({ where: { id: targetUserId }, data: { passwordHash: hash } });
    await this.logAudit({ userId: adminId, action: AuditAction.PASSWORD_RESET_REQUESTED, details: { targetUserId } });
    return { temporaryPassword: tempPassword };
  }
}
