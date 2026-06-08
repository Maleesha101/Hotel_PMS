import jwt from 'jsonwebtoken';
import crypto from 'crypto';
import { env } from '../config/env';
import { Role } from './enums';

export interface TokenPayload {
  sub: string; // user ID
  email: string;
  role: Role;
  name: string;
  iat?: number;
  exp?: number;
  jti?: string; // token ID for blocklist
}

export const signAccessToken = (payload: Omit<TokenPayload, 'iat' | 'exp' | 'jti'>): string => {
  const jti = crypto.randomUUID();
  return jwt.sign({ ...payload, jti }, env.JWT_PRIVATE_KEY, {
    algorithm: 'RS256',
    expiresIn: env.JWT_ACCESS_EXPIRY,
    issuer: 'hotel-pms-auth-service',
    audience: 'hotel-pms',
  });
};

export const signRefreshToken = (userId: string): string => {
  return jwt.sign({ sub: userId }, env.JWT_PRIVATE_KEY, {
    algorithm: 'RS256',
    expiresIn: env.JWT_REFRESH_EXPIRY,
    issuer: 'hotel-pms-auth-service',
    audience: 'hotel-pms-refresh',
  });
};

export const verifyAccessToken = (token: string): TokenPayload => {
  return jwt.verify(token, env.JWT_PUBLIC_KEY, {
    algorithms: ['RS256'],
    issuer: 'hotel-pms-auth-service',
    audience: 'hotel-pms',
  }) as TokenPayload;
};

export const verifyRefreshToken = (token: string): { sub: string } => {
  return jwt.verify(token, env.JWT_PUBLIC_KEY, {
    algorithms: ['RS256'],
    issuer: 'hotel-pms-auth-service',
    audience: 'hotel-pms-refresh',
  }) as { sub: string };
};

export const decodeTokenUnsafe = (token: string): TokenPayload | null => {
  return jwt.decode(token) as TokenPayload | null;
};
