import { prisma } from '../../config/prisma';
import bcrypt from 'bcryptjs';
import { ConflictError, ForbiddenError, NotFoundError } from '../../shared/errors';
import { AuditAction } from '../../shared/enums';
import { UserResponse, CreateUserDto, UpdateUserDto, UserFilters, Pagination } from './users.types';
import { logger } from '../../config/logger';
import { env } from '../../config/env';
import { AuthService } from '../auth/auth.service';

export class UsersService {
  private async logAudit(data: any) {
    await prisma.auditLog.create({ data });
  }

  private toResponse(user: any): UserResponse {
    const { id, name, email, role, status, phone, employeeId, department, lastLoginAt, loginCount, createdAt, updatedAt } = user;
    return { id, name, email, role, status, phone: phone ?? undefined, employeeId: employeeId ?? undefined, department: department ?? undefined, lastLoginAt: lastLoginAt ?? undefined, loginCount, createdAt, updatedAt };
  }

  async createUser(data: CreateUserDto, createdBy: string): Promise<UserResponse> {
    const hashed = await bcrypt.hash(data.password, env.BCRYPT_ROUNDS);
    try {
      const user = await prisma.user.create({
        data: {
          name: data.name,
          email: data.email,
          passwordHash: hashed,
          role: data.role as any,
          phone: data.phone,
          employeeId: data.employeeId,
          department: data.department,
          createdBy,
        },
      });
      await this.logAudit({ userId: createdBy, action: AuditAction.USER_CREATED, details: { targetUserId: user.id } });
      return this.toResponse(user);
    } catch (err: any) {
      // Prisma unique constraint violation code P2002
      if (err.code === 'P2002') {
        throw new ConflictError('Email already in use');
      }
      throw err;
    }
  }

  async listUsers(filters: UserFilters, pagination: Pagination): Promise<{ items: UserResponse[]; total: number }> {
    const where: any = {};
    if (filters.role) where.role = filters.role;
    if (filters.status) where.status = filters.status;
    if (filters.department) where.department = filters.department;

    const total = await prisma.user.count({ where });
    const items = await prisma.user.findMany({
      where,
      skip: (pagination.page - 1) * pagination.pageSize,
      take: pagination.pageSize,
    });
    return { items: items.map(this.toResponse), total };
  }

  async getUserById(id: string): Promise<UserResponse> {
    const user = await prisma.user.findUnique({ where: { id } });
    if (!user) throw new NotFoundError('User not found');
    return this.toResponse(user);
  }

  async updateUser(id: string, data: UpdateUserDto, updatedBy: string): Promise<UserResponse> {
    const existing = await prisma.user.findUnique({ where: { id } });
    if (!existing) throw new NotFoundError('User not found');
    const oldRole = existing.role;
    const updated = await prisma.user.update({
      where: { id },
      data: {
        name: data.name,
        role: data.role as any,
        phone: data.phone,
        department: data.department,
        status: data.status as any,
      },
    });
    if (data.role && data.role !== oldRole) {
      await this.logAudit({ userId: updatedBy, action: AuditAction.USER_UPDATED, details: { targetUserId: id, oldRole, newRole: data.role } });
    }
    return this.toResponse(updated);
  }

  async deactivateUser(id: string, adminId: string): Promise<void> {
    if (id === adminId) throw new ForbiddenError('Cannot modify your own account status');
    await prisma.user.update({ where: { id }, data: { status: 'INACTIVE' } });
    await this.logAudit({ userId: adminId, action: AuditAction.USER_DEACTIVATED, details: { targetUserId: id } });
  }

  async suspendUser(id: string, adminId: string): Promise<void> {
    if (id === adminId) throw new ForbiddenError('Cannot modify your own account status');
    await prisma.user.update({ where: { id }, data: { status: 'SUSPENDED' } });
    // Revoke all sessions for suspended user
    const authService = new AuthService();
    await authService.revokeAllSessions(id);
    await this.logAudit({ userId: adminId, action: AuditAction.USER_DEACTIVATED, details: { targetUserId: id, reason: 'suspend' } });
  }

  async activateUser(id: string, adminId: string): Promise<void> {
    await prisma.user.update({ where: { id }, data: { status: 'ACTIVE' } });
    await this.logAudit({ userId: adminId, action: AuditAction.USER_UPDATED, details: { targetUserId: id, status: 'ACTIVE' } });
  }
}
