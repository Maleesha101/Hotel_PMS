export interface UserResponse {
  id: string;
  name: string;
  email: string;
  role: string;
  status: string;
  phone?: string;
  employeeId?: string;
  department?: string;
  lastLoginAt?: Date;
  loginCount: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface CreateUserDto {
  name: string;
  email: string;
  password: string;
  role: string;
  phone?: string;
  employeeId?: string;
  department?: string;
}

export interface UpdateUserDto {
  name?: string;
  role?: string;
  phone?: string;
  department?: string;
  status?: string;
}

export interface UserFilters {
  role?: string;
  status?: string;
  department?: string;
}

export interface Pagination {
  page: number;
  pageSize: number;
}
