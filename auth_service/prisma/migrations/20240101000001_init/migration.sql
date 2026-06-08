-- Prisma migration to create initial database schema for Auth Service

-- Create enums
CREATE TYPE "Role" AS ENUM ('ADMIN', 'FRONT_DESK', 'HOUSEKEEPING', 'MAINTENANCE', 'ACCOUNTANT');
CREATE TYPE "UserStatus" AS ENUM ('ACTIVE', 'INACTIVE', 'SUSPENDED');
CREATE TYPE "AuditAction" AS ENUM (
  'LOGIN',
  'LOGOUT',
  'LOGIN_FAILED',
  'TOKEN_REFRESHED',
  'TOKEN_REVOKED',
  'USER_CREATED',
  'USER_UPDATED',
  'USER_DEACTIVATED',
  'PASSWORD_CHANGED',
  'PASSWORD_RESET_REQUESTED'
);

-- Users table
CREATE TABLE "users" (
  "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "name" TEXT NOT NULL,
  "email" TEXT NOT NULL UNIQUE,
  "passwordHash" TEXT NOT NULL,
  "role" "Role" NOT NULL,
  "status" "UserStatus" NOT NULL DEFAULT 'ACTIVE',
  "phone" TEXT,
  "employeeId" TEXT UNIQUE,
  "department" TEXT,
  "lastLoginAt" TIMESTAMP,
  "loginCount" INT NOT NULL DEFAULT 0,
  "createdBy" TEXT,
  "createdAt" TIMESTAMP NOT NULL DEFAULT now(),
  "updatedAt" TIMESTAMP NOT NULL DEFAULT now()
);
CREATE INDEX "users_role_idx" ON "users" ("role");
CREATE INDEX "users_status_idx" ON "users" ("status");

-- Refresh tokens table
CREATE TABLE "refresh_tokens" (
  "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "userId" UUID NOT NULL REFERENCES "users"("id") ON DELETE CASCADE,
  "tokenHash" TEXT NOT NULL UNIQUE,
  "deviceInfo" TEXT,
  "ipAddress" TEXT,
  "expiresAt" TIMESTAMP NOT NULL,
  "revokedAt" TIMESTAMP,
  "createdAt" TIMESTAMP NOT NULL DEFAULT now()
);
CREATE INDEX "refresh_tokens_user_idx" ON "refresh_tokens" ("userId");
CREATE INDEX "refresh_tokens_expires_idx" ON "refresh_tokens" ("expiresAt");

-- Audit logs table
CREATE TABLE "audit_logs" (
  "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "userId" UUID REFERENCES "users"("id") ON DELETE SET NULL,
  "action" "AuditAction" NOT NULL,
  "ipAddress" TEXT,
  "userAgent" TEXT,
  "details" JSONB,
  "success" BOOLEAN NOT NULL DEFAULT true,
  "createdAt" TIMESTAMP NOT NULL DEFAULT now()
);
CREATE INDEX "audit_logs_user_idx" ON "audit_logs" ("userId");
CREATE INDEX "audit_logs_action_idx" ON "audit_logs" ("action");
CREATE INDEX "audit_logs_created_idx" ON "audit_logs" ("createdAt");
