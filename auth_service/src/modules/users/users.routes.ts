import { Router } from 'express';
import { createUser, listUsers, getUser, updateUser, deactivateUser, suspendUser, activateUser } from './users.controller';
import { authenticate } from '../../middleware/authenticate';
import { authorize } from '../../middleware/authorize';
import { validate } from '../../middleware/validate';
import { createUserSchema, updateUserSchema, listUsersSchema } from './users.schema';

const router = Router();

/**
 * @swagger
 * tags:
 *   - name: Users
 *     description: User management endpoints
 */

/**
 * @swagger
 * /api/v1/users:
 *   post:
 *     tags: [Users]
 *     security:
 *       - BearerAuth: []
 *     summary: Create a new staff user (ADMIN only)
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema: $ref: '#/components/schemas/CreateUserRequest'
 *     responses:
 *       201:
 *         description: User created
 *       403:
 *         description: Forbidden
 */
router.post('/', authenticate, authorize('ADMIN'), validate(createUserSchema), createUser);

/**
 * @swagger
 * /api/v1/users:
 *   get:
 *     tags: [Users]
 *     security:
 *       - BearerAuth: []
 *     summary: List users with optional filters and pagination (ADMIN only)
 *     parameters:
 *       - in: query
 *         name: role
 *         schema:
 *           type: string
 *       - in: query
 *         name: status
 *         schema:
 *           type: string
 *       - in: query
 *         name: department
 *         schema:
 *           type: string
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *           default: 1
 *       - in: query
 *         name: pageSize
 *         schema:
 *           type: integer
 *           default: 20
 *     responses:
 *       200:
 *         description: List of users
 */
router.get('/', authenticate, authorize('ADMIN'), validate(listUsersSchema), listUsers);

/**
 * @swagger
 * /api/v1/users/{id}:
 *   get:
 *     tags: [Users]
 *     security:
 *       - BearerAuth: []
 *     summary: Get user profile by ID (ADMIN only)
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: User profile
 */
router.get('/:id', authenticate, authorize('ADMIN'), getUser);

/**
 * @swagger
 * /api/v1/users/{id}:
 *   patch:
 *     tags: [Users]
 *     security:
 *       - BearerAuth: []
 *     summary: Update user info (ADMIN only)
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema: $ref: '#/components/schemas/UpdateUserRequest'
 *     responses:
 *       200:
 *         description: User updated
 */
router.patch('/:id', authenticate, authorize('ADMIN'), validate(updateUserSchema), updateUser);

/**
 * @swagger
 * /api/v1/users/{id}:
 *   delete:
 *     tags: [Users]
 *     security:
 *       - BearerAuth: []
 *     summary: Deactivate (soft delete) user (ADMIN only)
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: User deactivated
 */
router.delete('/:id', authenticate, authorize('ADMIN'), deactivateUser);

/**
 * @swagger
 * /api/v1/users/{id}/suspend:
 *   post:
 *     tags: [Users]
 *     security:
 *       - BearerAuth: []
 *     summary: Suspend a user and revoke sessions (ADMIN only)
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: User suspended
 */
router.post('/:id/suspend', authenticate, authorize('ADMIN'), suspendUser);

/**
 * @swagger
 * /api/v1/users/{id}/activate:
 *   post:
 *     tags: [Users]
 *     security:
 *       - BearerAuth: []
 *     summary: Reactivate a suspended or inactive user (ADMIN only)
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: User activated
 */
router.post('/:id/activate', authenticate, authorize('ADMIN'), activateUser);

export default router;
