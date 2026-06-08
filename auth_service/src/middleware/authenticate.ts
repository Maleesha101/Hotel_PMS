import { Request, Response, NextFunction } from 'express';
import { verifyAccessToken } from '../shared/jwt';
import { redis } from '../config/redis';
import { UnauthorizedError } from '../shared/errors';

export const authenticate = async (req: Request, _res: Response, next: NextFunction) => {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith('Bearer ')) {
    return next(new UnauthorizedError('No token provided'));
  }
  const token = authHeader.split(' ')[1];

  // Check blocklist
  const isBlocklisted = await redis.get(`blocklist:${token}`);
  if (isBlocklisted) {
    return next(new UnauthorizedError('Token has been revoked'));
  }

  try {
    const payload = verifyAccessToken(token);
    req.user = payload;
    next();
  } catch (err) {
    return next(err);
  }
};