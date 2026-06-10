import swaggerJsdoc from 'swagger-jsdoc';
import swaggerUi from 'swagger-ui-express';
import { Express } from 'express';

const options: swaggerJsdoc.Options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Hotel PMS — Auth & User Service API',
      version: '1.0.0',
      description: `
## Overview
Central authentication and identity service for the Hotel Property Management System.

Issues RS256-signed JWTs consumed by all downstream services:
- Reservation Service (port 8081)
- Housekeeping Service (port 8082)
- Maintenance Service (port 8083)
- Invoice Service (port 8084)

## Auth Flow
1. POST /api/v1/auth/login → receive accessToken + refreshToken
2. Include accessToken in \`Authorization: Bearer <token>\` header
3. Refresh before expiry via POST /api/v1/auth/refresh

## Token Lifetime
- Access token: 15 minutes
- Refresh token: 7 days (rotated on each use)
      `,
      contact: { name: 'Hotel PMS Team' },
    },
    servers: [{ url: 'http://localhost:8080', description: 'Local development' }],
    components: {
      securitySchemes: {
        BearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT',
          description: 'RS256 JWT access token issued by this service',
        },
      },
      schemas: {
        ApiResponse: {
          type: 'object',
          properties: {
            success: { type: 'boolean', example: true },
            data: { type: 'object' },
            message: { type: 'string' },
          },
        },
        PaginationMeta: {
          type: 'object',
          properties: {
            total: { type: 'integer', example: 42 },
            page: { type: 'integer', example: 1 },
            pageSize: { type: 'integer', example: 20 },
            totalPages: { type: 'integer', example: 3 },
          },
        },
      },
    },
    security: [{ BearerAuth: [] }],
  },
  apis: [
    process.env.NODE_ENV === 'production' || __filename.endsWith('.js')
      ? './dist/modules/**/*.routes.js' 
      : './src/modules/**/*.routes.ts'
  ],
};

export const setupSwagger = (app: Express): void => {
  const spec = swaggerJsdoc(options);
  app.use('/swagger-ui.html', swaggerUi.serve, swaggerUi.setup(spec, {
    customSiteTitle: 'Hotel PMS Auth API',
    swaggerOptions: {
      persistAuthorization: true,
      displayRequestDuration: true,
      tryItOutEnabled: true,
    },
  }));
  app.get('/v3/api-docs', (_req, res) => res.json(spec));
};
