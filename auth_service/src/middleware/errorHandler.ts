import { Request, Response, NextFunction } from 'express';
import { AppError } from '../shared/errors';
import { logger } from '../config/logger';

export const errorHandler = (err: Error, req: Request, res: Response, _next: NextFunction) => {
  if (err instanceof AppError) {
    logger.warn({ message: err.message, statusCode: err.statusCode, path: req.path });
    return res.status(err.statusCode).json({ success: false, error: err.message });
  }

  // JWT-specific errors
  if (err.name === 'JsonWebTokenError') {
    return res.status(401).json({ success: false, error: 'Invalid token' });
  }
  if (err.name === 'TokenExpiredError') {
    return res.status(401).json({ success: false, error: 'Token has expired' });
  }

  logger.error({ message: err.message, stack: err.stack, path: req.path });
  return res.status(500).json({ success: false, error: 'Internal server error' });
};