# Auth Service

This repository implements the **Auth & User Management Microservice** for the Hotel Property Management System (PMS). It provides:

- User account lifecycle (create, update, deactivate, password management)
- Role‑Based Access Control (RBAC) for five staff roles
- Stateless JWT authentication using RS256 asymmetric signing
- Refresh‑token rotation with Redis‑backed revocation and blocklisting
- Comprehensive audit logging of all auth events and admin actions
- OpenAPI 3 documentation via Swagger UI

## Prerequisites

- **Node.js 20 LTS**
- **Docker** (for containerised development)
- **PostgreSQL 15** (or use the provided Docker compose service)
- **Redis 7** (or use the provided Docker compose service)

## Project Setup (local development)

```bash
# Clone the repo and cd into it
git clone <repo-url>
cd "Hotel PMS/auth_service"

# Install dependencies
npm install

# Generate RSA key pair (run once)
npm run gen-keys > keys.txt
# Copy the printed PEM strings into a .env file (or set them in your environment)
# For convenience you can copy the example values from .env.example

# Set up environment variables
cp .env.example .env   # edit .env and replace the key placeholders with the actual PEMs

# Initialise the database schema
npx prisma migrate dev --name init

# Seed development users (if running locally)
npm run seed

# Start the service in dev mode (ts-node-dev) – listens on ${PORT:-8081}
npm run dev
```

The health endpoint should respond:

```bash
curl http://localhost:8081/health
# => {"status":"ok","uptime":...}
```

Swagger UI is available at:

```
http://localhost:8081/swagger-ui.html
```

## Docker Development

The service can be run entirely inside Docker:

```bash
docker-compose up --build
```

- Auth Service: `http://localhost:8081`
- PostgreSQL: `postgresql://postgres:postgres@postgres:5432/auth_db`
- Redis: `redis://redis:6379`

**To initialize the database and seed inside Docker:**
1. `docker-compose exec auth-service npm run migrate:prod`
2. `docker-compose exec auth-service npm run seed:docker`

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NODE_ENV` | Runtime environment | `development` |
| `PORT` | HTTP port | `8081` |
| `DATABASE_URL` | Prisma connection string | `postgresql://postgres:postgres@postgres:5432/auth_db` |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379` |
| `JWT_PRIVATE_KEY` | RSA private key (PEM) used for signing tokens |
| `JWT_PUBLIC_KEY` | RSA public key (PEM) distributed to downstream services |
| `JWT_ACCESS_EXPIRY` | Access token TTL (e.g., `15m`) |
| `JWT_REFRESH_EXPIRY` | Refresh token TTL (e.g., `7d`) |
| `BCRYPT_ROUNDS` | bcrypt work factor (default `12`) |
| `ADMIN_SEED_EMAIL` | Default admin user (dev) |
| `ADMIN_SEED_PASSWORD` | Default admin password |
| `ADMIN_SEED_NAME` | Default admin name |

See `.env.example` for the full list.

## Testing

```bash
npm test            # run unit and integration tests
npm run test:watch  # watch mode
```

## Scripts

- `npm run gen-keys` – generates a 2048‑bit RSA key pair (private and public PEMs).
- `npm run migrate` – runs Prisma migrations.
- `npm run seed` – seeds the development database with initial staff users.

## API Documentation

All routes are documented using Swagger JSDoc comments. Open the Swagger UI at `/swagger-ui.html` or retrieve the raw OpenAPI spec at `/v3/api-docs`.

## License

MIT © Hotel PMS Team