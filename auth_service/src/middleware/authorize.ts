import { Request, Response, NextFunction } from 'express';
import { Role } from '../shared/enums';
import { ForbiddenError } from '../shared/errors';

export const authorize = (...allowedRoles: Role[]) =>
  (req: Request, _res: Response, next: NextFunction) => {
    if (!req.user) {
      return next(new ForbiddenError('Not authenticated'));
    }
    if (!allowedRoles.includes(req.user.role as Role)) {
      return next(new ForbiddenError(`Role '${req.user.role}' is not permitted for this action`));
    }
    next();
  };
