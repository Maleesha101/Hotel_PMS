import { AuditAction } from '../../shared/enums';

export interface AuditLogCreateDto {
  userId?: string;
  action: AuditAction;
  ipAddress?: string;
  userAgent?: string;
  details?: any;
  success?: boolean;
}