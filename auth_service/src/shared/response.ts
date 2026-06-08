export const success = <T>(data: T, message = 'Success') => ({
  success: true,
  message,
  data,
});

export const paginated = <T>(items: T[], meta: { total: number; page: number; pageSize: number; totalPages: number }, message = 'Success') => ({
  success: true,
  message,
  data: items,
  meta,
});
