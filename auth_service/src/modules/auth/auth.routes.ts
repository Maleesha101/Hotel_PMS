import { Router } from 'express';
import { login, logout, refresh, verify, me, changePassword, revokeAll, adminResetPassword } from './auth.controller';
import { validate } from '../../middleware/validate';
import { loginRateLimiter, refreshRateLimiter } from '../../middleware/rateLimiter';
import { authenticate } from '../../middleware/authenticate';
import { authorize } from '../../middleware/authorize';
import { loginSchema, refreshSchema, verifySchema, changePasswordSchema } from './auth.schema';
import { Role } from '../../shared/enums';

const router = Router();

/**
 * @swagger
 * tags:
 *   - name: Auth
 *     description: Authentication and token management
 */

/**
 * @swagger
 * /api/v1/auth/login:
 *   post:
 *     tags: [Auth]
 *     summary: Authenticate a staff user
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema: $ref: '#/components/schemas/LoginRequest'
 *     responses:
 *       200:
 *         description: Login successful, returns access and refresh tokens
 *       401:
 *         description: Invalid credentials
 */
router.post('/login', loginRateLimiter, validate(loginSchema), login);

/**
 * @swagger
 * /api/v1/auth/logout:
 *   post:
 *     tags: [Auth]
 *     security:
 *       - BearerAuth: []
 *     summary: Revoke current access token and all refresh tokens for the user
 *     responses:
 *       200:
 *         description: Logged out successfully
 */
router.post('/logout', authenticate, logout);

/**
 * @swagger
 * /api/v1/auth/refresh:
 *   post:
 *     tags: [Auth]
 *     summary: Refresh access token using a rotating refresh token
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema: $ref: '#/components/schemas/RefreshRequest'
 *     responses:
 *       200:
 *         description: New token pair issued
 *       401:
 *         description: Invalid refresh token
 */
router.post('/refresh', refreshRateLimiter, validate(refreshSchema), refresh);

/**
 * @swagger
 * /api/v1/auth/verify:
 *   post:
 *     tags: [Auth]
 *     summary: Verify a JWT token's validity
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema: $ref: '#/components/schemas/VerifyRequest'
 *     responses:
 *       200:
 *         description: Token payload returned
 */
router.post('/verify', validate(verifySchema), verify);

/**
 * @swagger
 * /api/v1/auth/me:
 *   get:
 *     tags: [Auth]
 *     security:
 *       - BearerAuth: []
 *     summary: Get current authenticated user profile
 *     responses:
 *       200:
 *         description: User profile data
 *       401:
 *         description: Unauthorized
 */
router.get('/me', authenticate, me);

/**
 * @swagger
 * /api/v1/auth/change-password:
 *   post:
 *     tags: [Auth]
 *     security:
 *       - BearerAuth: []
 *     summary: Change own password
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema: $ref: '#/components/schemas/ChangePasswordRequest'
 *     responses:
 *       200:
 *         description: Password changed
 */
router.post('/change-password', authenticate, validate(changePasswordSchema), changePassword);

/**
 * @swagger
 * /api/v1/auth/revoke-all-sessions:
 *   post:
 *     tags: [Auth]
 *     security:
 *       - BearerAuth: []
 *     summary: Revoke all refresh tokens for the authenticated user
 *     responses:
 *       200:
 *         description: All sessions revoked
 */
router.post('/revoke-all-sessions', authenticate, revokeAll);

/**
 * @swagger
 * /api/v1/auth/admin/reset-password/{id}:
 *   post:
 *     tags: [Auth]
 *     security:
 *       - BearerAuth: []
 *     summary: Admin resets a user's password to a temporary one
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: Target user ID
 *     responses:
 *       200:
 *         description: Temporary password returned
 */
router.post('/admin/reset-password/:id', authenticate, authorize(Role.ADMIN), adminResetPassword);

export default router;
