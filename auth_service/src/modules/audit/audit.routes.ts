import { Router } from 'express';
import { listAudits, getUserAudits } from './audit.controller';
import { authenticate } from '../../middleware/authenticate';
import { authorize } from '../../middleware/authorize';
import { Role } from '../../shared/enums';

const router = Router();

/**
 * @swagger
 * tags:
 *   - name: Audit
 *     description: Audit log endpoints
 */

/**
 * @swagger
 * /api/v1/audit:
 *   get:
 *     tags: [Audit]
 *     security:
 *       - BearerAuth: []
 *     summary: List audit logs with filters
 *     parameters:
 *       - in: query
 *         name: userId
 *         schema:
 *           type: string
 *       - in: query
 *         name: action
 *         schema:
 *           type: string
 *       - in: query
 *         name: success
 *         schema:
 *           type: boolean
 *       - in: query
 *         name: startDate
 *         schema:
 *           type: string
 *           format: date-time
 *       - in: query
 *         name: endDate
 *         schema:
 *           type: string
 *           format: date-time
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
 *         description: Paginated audit logs
 */
router.get('/', authenticate, authorize(Role.ADMIN), listAudits);

/**
 * @swagger
 * /api/v1/audit/user/{id}:
 *   get:
 *     tags: [Audit]
 *     security:
 *       - BearerAuth: []
 *     summary: Get audit logs for a specific user
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
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
 *         description: Paginated user audit logs
 */
router.get('/user/:id', authenticate, authorize(Role.ADMIN), getUserAudits);

export default router;
