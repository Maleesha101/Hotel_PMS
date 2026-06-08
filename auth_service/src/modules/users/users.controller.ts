import { Request, Response, NextFunction } from 'express';
import { UsersService } from './users.service';
import { success, paginated } from '../../shared/response';
import { CreateUserDto, UpdateUserDto } from './users.types';

const usersService = new UsersService();

export const createUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const data: CreateUserDto = req.body;
    const createdBy = req.user?.sub as string;
    const user = await usersService.createUser(data, createdBy);
    res.json(success(user, 'User created'));
  } catch (err) {
    next(err);
  }
};

export const listUsers = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const filters = {
      role: req.query.role as string | undefined,
      status: req.query.status as string | undefined,
      department: req.query.department as string | undefined,
    };
    const pagination = {
      page: Number(req.query.page) || 1,
      pageSize: Number(req.query.pageSize) || 20,
    };
    const { items, total } = await usersService.listUsers(filters, pagination);
    const meta = { total, page: pagination.page, pageSize: pagination.pageSize, totalPages: Math.ceil(total / pagination.pageSize) };
    res.json(paginated(items, meta));
  } catch (err) {
    next(err);
  }
};

export const getUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const user = await usersService.getUserById(req.params.id);
    res.json(success(user));
  } catch (err) {
    next(err);
  }
};

export const updateUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const data: UpdateUserDto = req.body;
    const updatedBy = req.user?.sub as string;
    const user = await usersService.updateUser(req.params.id, data, updatedBy);
    res.json(success(user, 'User updated'));
  } catch (err) {
    next(err);
  }
};

export const deactivateUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const adminId = req.user?.sub as string;
    await usersService.deactivateUser(req.params.id, adminId);
    res.json(success(null, 'User deactivated'));
  } catch (err) {
    next(err);
  }
};

export const suspendUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const adminId = req.user?.sub as string;
    await usersService.suspendUser(req.params.id, adminId);
    res.json(success(null, 'User suspended'));
  } catch (err) {
    next(err);
  }
};

export const activateUser = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const adminId = req.user?.sub as string;
    await usersService.activateUser(req.params.id, adminId);
    res.json(success(null, 'User activated'));
  } catch (err) {
    next(err);
  }
};
