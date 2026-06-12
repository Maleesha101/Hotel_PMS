import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import { env } from './env'; // Corrected path
import { requestLogger } from '../middleware/requestLogger'; // Corrected path
import { generalRateLimiter } from '../middleware/rateLimiter'; // Corrected path
import { errorHandler } from '../middleware/errorHandler'; // Corrected path
import authRouter from '../modules/auth/auth.routes'; // Corrected path
import usersRouter from '../modules/users/users.routes'; // Corrected path
import auditRouter from '../modules/audit/audit.routes'; // Corrected path
import { setupSwagger } from './swagger'; // Corrected path

const app = express();

// Global middlewares
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'", "'unsafe-eval'"], // Required for Swagger UI
      styleSrc: ["'self'", "'unsafe-inline'"], // Required for Swagger UI
      imgSrc: ["'self'", "data:", "validator.swagger.io"],
      connectSrc: ["'self'", `http://localhost:${env.PORT}`, `http://127.0.0.1:${env.PORT}`], // Consolidated connect-src
    },
  },
}));
const allowedOrigins = env.ALLOWED_ORIGINS 
  ? env.ALLOWED_ORIGINS.split(',').map((o: string) => o.trim()) // Added explicit type for 'o'
  : '*';

app.use(cors({ 
  origin: (requestOrigin, callback) => {
    // Allow same-origin requests (origin is undefined) or allowed list
    if (!requestOrigin) {
      return callback(null, true);
    }

    if (allowedOrigins === '*') {
      return callback(null, true);
    }

    if (Array.isArray(allowedOrigins) && allowedOrigins.includes(requestOrigin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true
}));
app.use(compression());
app.use(express.json());
app.use(express.urlencoded({ extended: true })); // Ensure this is correctly called with app.use
app.use(requestLogger);
app.use(generalRateLimiter);

// Health endpoints
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', uptime: process.uptime(), timestamp: new Date().toISOString() });
});

app.get('/health/ready', async (_req, res) => {
  try {
    // Check DB connection
    const { prisma } = await import('./prisma'); // Corrected path
    await prisma.$queryRaw`SELECT 1`;
    // Check Redis
    const { redis } = await import('./redis'); // Corrected path
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
