import { Request, Response, NextFunction } from 'express';
import { AuthService } from './auth.service';
import { LoginResponse, TokenPair } from './auth.types';
import { success } from '../../shared/response';

const authService = new AuthService();

export const login = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { email, password } = req.body;
    const meta = { ipAddress: req.ip, userAgent: req.get('User-Agent'), deviceInfo: undefined };
    const result = await authService.login(email, password, meta);
    res.json(success(result));
  } catch (err) {
    next(err);
  }
};

export const logout = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const accessToken = req.headers.authorization?.split(' ')[1] || '';
    const userId = req.user?.sub as string;
    await authService.logout(accessToken, userId);
    res.json(success(null, 'Logged out'));
  } catch (err) {
    next(err);
  }
};

export const refresh = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { refreshToken } = req.body;
    const meta = { ipAddress: req.ip, userAgent: req.get('User-Agent'), deviceInfo: undefined };
    const tokens = await authService.refreshTokens(refreshToken, meta);
    res.json(success(tokens));
  } catch (err) {
    next(err);
  }
};

export const verify = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { token } = req.body;
    const payload = await authService.verifyToken(token);
    res.json(success(payload));
  } catch (err) {
    next(err);
  }
};

export const me = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const user = req.user!;
    res.json(success({ id: user.sub, email: user.email, name: user.name, role: user.role }));
  } catch (err) {
    next(err);
  }
};

export const changePassword = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const userId = req.user!.sub as string;
    const { currentPassword, newPassword } = req.body;
    await authService.changePassword(userId, currentPassword, newPassword);
    res.json(success(null, 'Password changed'));
  } catch (err) {
    next(err);
  }
};

export const revokeAll = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const userId = req.user!.sub as string;
    await authService.revokeAllSessions(userId);
    res.json(success(null, 'All sessions revoked'));
  } catch (err) {
    next(err);
  }
};

export const adminResetPassword = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const adminId = req.user!.sub as string;
    const { id: targetUserId } = req.params;
    const result = await authService.adminResetPassword(targetUserId, adminId);
    res.json(success(result, 'Temporary password generated'));
  } catch (err) {
    next(err);
  }
};
