export class AppError extends Error {
  public statusCode: number;
  public isOperational: boolean;
  constructor(message: string, statusCode = 500, isOperational = true) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = isOperational;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class BadRequestError extends AppError {
  constructor(message: string) { super(message, 400); }
}

export class UnauthorizedError extends AppError {
  constructor(message: string) { super(message, 401); }
}

export class ForbiddenError extends AppError {
  constructor(message: string) { super(message, 403); }
}

export class NotFoundError extends AppError {
  constructor(message: string) { super(message, 404); }
}

export class ConflictError extends AppError {
  constructor(message: string) { super(message, 409); }
}

export class ValidationError extends AppError {
  constructor(message: string) { super(message, 422); }
}
