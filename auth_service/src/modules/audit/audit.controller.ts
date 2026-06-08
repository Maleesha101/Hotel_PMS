import { Request, Response, NextFunction } from 'express';
import { AuditService } from './audit.service';
import { success, paginated } from '../../shared/response';

const auditService = new AuditService();

export const listAudits = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { userId, action, success: successQuery, startDate, endDate, page = '1', pageSize = '20' } = req.query as any;
    const result = await auditService.list({
      userId,
      action,
      success: successQuery !== undefined ? successQuery === 'true' : undefined,
      startDate: startDate ? new Date(startDate) : undefined,
      endDate: endDate ? new Date(endDate) : undefined,
      page: Number(page),
      pageSize: Number(pageSize),
    });
    const meta = { total: result.total, page: Number(page), pageSize: Number(pageSize), totalPages: Math.ceil(result.total / Number(pageSize)) };
    res.json(paginated(result.logs, meta));
  } catch (err) {
    next(err);
  }
};

export const getUserAudits = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { id } = req.params;
    const { page = '1', pageSize = '20' } = req.query as any;
    const result = await auditService.list({ userId: id, page: Number(page), pageSize: Number(pageSize) });
    const meta = { total: result.total, page: Number(page), pageSize: Number(pageSize), totalPages: Math.ceil(result.total / Number(pageSize)) };
    res.json(paginated(result.logs, meta));
  } catch (err) {
    next(err);
  }
};
