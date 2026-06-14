import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.coerce.number().default(8081),

  DATABASE_URL: z.string().url(),

  REDIS_URL: z.string().default('redis://localhost:6381'),

  JWT_PRIVATE_KEY: z.string().min(1),
  JWT_PUBLIC_KEY: z.string().min(1),
  JWT_ACCESS_EXPIRY: z.string().default('15m'),
  JWT_REFRESH_EXPIRY: z.string().default('7d'),

  BCRYPT_ROUNDS: z.coerce.number().default(12),

  ADMIN_SEED_EMAIL: z.string().email().default('admin@hotelpms.com'),
  ADMIN_SEED_PASSWORD: z.string().min(8).default('Admin@1234!'),
  ADMIN_SEED_NAME: z.string().default('System Admin'),

  // Optional: allowed origins for CORS, comma separated
  ALLOWED_ORIGINS: z.string().optional(),
});

const result = envSchema.safeParse(process.env);
if (!result.success) {
  console.error('❌ Invalid environment variables:', result.error.flatten().fieldErrors);
  process.exit(1);
}

export const env = result.data;
