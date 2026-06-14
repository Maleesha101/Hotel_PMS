import { prisma } from '../../config/prisma';
import { AuditAction } from '../../shared/enums';
import { AuditLogCreateDto } from './audit.types';
import { logger } from '../../config/logger';

export class AuditService {
  async log(data: AuditLogCreateDto) {
    await prisma.auditLog.create({ data });
  }

  async list(params: { userId?: string; action?: AuditAction; success?: boolean; startDate?: Date; endDate?: Date; page: number; pageSize: number }) {
    const { userId, action, success, startDate, endDate, page, pageSize } = params;
    const where: any = {};
    if (userId) where.userId = userId;
    if (action) where.action = action;
    if (typeof success === 'boolean') where.success = success;
    if (startDate || endDate) where.createdAt = {};
    if (startDate) where.createdAt.gte = startDate;
    if (endDate) where.createdAt.lte = endDate;

    const total = await prisma.auditLog.count({ where });
    const logs = await prisma.auditLog.findMany({
      where,
      orderBy: { createdAt: 'desc' },
      skip: (page - 1) * pageSize,
      take: pageSize,
    });
    return { total, logs };
  }
}
