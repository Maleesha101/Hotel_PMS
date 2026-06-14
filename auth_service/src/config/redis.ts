import Redis from 'ioredis';
import { env } from './env';

export const redis = new Redis(env.REDIS_URL);

// Optional: handle connection events for logging
redis.on('error', (err) => {
  console.error('Redis error:', err);
});
