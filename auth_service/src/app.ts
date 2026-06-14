import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import { env } from './config/env';
import { requestLogger } from './middleware/requestLogger';
import { generalRateLimiter } from './middleware/rateLimiter';
import { errorHandler } from './middleware/errorHandler';
import authRouter from './modules/auth/auth.routes';
import usersRouter from './modules/users/users.routes';
import auditRouter from './modules/audit/audit.routes';
import { setupSwagger } from './config/swagger';

const app = express();

// Global middlewares
app.use(helmet({
  // Disable CSP for Swagger UI to work correctly; in production, configure specifically if needed
  contentSecurityPolicy: false,
}));
const allowedOrigins = env.ALLOWED_ORIGINS 
  ? env.ALLOWED_ORIGINS.split(',').map(o => o.trim()) 
  : '*';
app.use(cors({ 
  origin: allowedOrigins === '*' ? true : allowedOrigins,
  credentials: true
}));
app.use(compression());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(requestLogger);
app.use(generalRateLimiter);

// Health endpoints
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', uptime: process.uptime(), timestamp: new Date().toISOString() });
});

app.get('/health/ready', async (_req, res) => {
  try {
    // Check DB connection
    const { prisma } = await import('./config/prisma');
    await prisma.$queryRaw`SELECT 1`;
    // Check Redis
    const { redis } = await import('./config/redis');
    await redis.ping();
    res.status(200).json({ status: 'ready' });
  } catch (e) {
    res.status(503).json({ status: 'unavailable', error: (e as Error).message });
  }
});

// API routes
app.use('/api/v1/auth', authRouter);
app.use('/api/v1/users', usersRouter);
app.use('/api/v1/audit', auditRouter);

// Swagger UI
setupSwagger(app);

// Global error handler (must be after routes)
app.use(errorHandler);

export default app;
