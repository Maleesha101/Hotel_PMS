# 🏨 Housekeeping Service

**A FastAPI‑based microservice for managing room status, supplies, inventory, and damage reports** within the Hotel PMS suite.

---

## 📖 Table of Contents
- [Overview](#overview)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [Quick Start (Docker Compose)](#quick-start-docker-compose)
- [Running Locally (without Docker)](#running‑locally)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [OpenAPI Docs](#openapi-docs)
- [Development Workflow](#development‑workflow)
- [Testing](#testing)
- [Database Migrations](#database-migrations)
- [Logging & Monitoring](#logging--monitoring)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview
The **Housekeeping Service** provides a RESTful JSON API for:
- Creating, reading, updating and bulk‑updating **room status** records.
- Managing **room supply standards** (items required per room type).
- Basic **inventory** and **damage report** endpoints (stubs ready for extension).
- Publishing every status change to a Redis channel (`ROOM_STATUS_CHANNEL`) for downstream consumers (e.g., front‑desk UI, mobile housekeeping app).
- Enforcing role‑based access – all endpoints currently require the **Admin** role.

---

## Architecture & Tech Stack
| Layer | Technology |
|-------|------------|
| **Web framework** | FastAPI 0.111.0 |
| **ASGI server** | Uvicorn (workers = 2) |
| **Database** | PostgreSQL 15 (async via `asyncpg`) + SQLAlchemy 2.x async ORM |
| **Message broker** | Redis 5.0.4 (pub/sub) |
| **Event streaming** | Kafka (KRaft mode) – only needed by other services |
| **Containerisation** | Docker (multi‑stage build) |
| **Configuration** | Pydantic‑Settings (`app.config.settings`) |
| **Testing** | Pytest (unit & integration) |
| **Linting / Formatting** | Ruff, Black, isort |

---

## Quick Start (Docker Compose)
**Prerequisites** – Docker ≥ 20.10 and Docker‑Compose ≥ 2.0 installed.
```bash
# Clone the repository (if you haven't yet)
git clone https://github.com/your-org/hotel-pms.git
cd "Hotel PMS/housekeeping_service"

# Build and start the whole stack (Postgres, Redis, Kafka, and the service)
# The service will be reachable at http://localhost:8082
docker compose up --build
```
The UI for the API is available at:
```
http://localhost:8082/swagger-ui.html   # Swagger UI (interactive)
http://localhost:8082/v3/api-docs      # Raw OpenAPI JSON
```

---

## Running Locally (without Docker)
1. **Create a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate
```
2. **Install dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
3. **Start supporting services** (easiest via Docker)
```bash
# Run only the dependencies
docker compose up postgres redis kafka -d
```
4. **Export required environment variables** and run the API
```bash
export DB_URL=postgresql+asyncpg://postgres:postgres@localhost:5434/housekeeping_db
export REDIS_URL=redis://localhost:6380/0
export KAFKA_BOOTSTRAP=localhost:9092
export ENVIRONMENT=dev
export JWT_PUBLIC_KEY="<your‑public‑key>"
# optional custom values defined in app.config.settings …
uvicorn app.main:app --host 0.0.0.0 --port 8082 --workers 2
```
---

## Environment Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `DB_URL` | Async SQLAlchemy connection string | `postgresql+asyncpg://postgres:postgres@postgres:5432/housekeeping_db` |
| `REDIS_URL` | Redis connection string (pub/sub) | `redis://redis:6379/0` |
| `KAFKA_BOOTSTRAP` | Kafka broker address (required by config) | `kafka:9092` |
| `ENVIRONMENT` | Runtime environment (`dev`, `staging`, `prod`) | `dev` |
| `JWT_PUBLIC_KEY` | Public key for JWT verification (used by auth middleware) | `-----BEGIN PUBLIC KEY-----\n...` |
| `ROOM_STATUS_CHANNEL` *(optional)* | Redis channel name for status events | `room_status_updates` |
| `LOG_LEVEL` *(optional)* | Python logging level (`INFO`, `DEBUG`, …) | `INFO` |
All variables are defined via **Pydantic‑Settings** in `app/config.py`; missing required variables cause an early startup error.
---

## API Reference
All endpoints are prefixed with `/api/v1`.
### Room Status (`/room/status`)
| Method | Path | Description | Request Body | Response |
|--------|------|-------------|--------------|----------|
| `GET` | `/rooms/status` | List rooms with optional filters (`status`, `floor`, `room_type`) | – | `{status:"success", data:[RoomStatusResponse,…]}` |
| `GET` | `/rooms/status/{room_id}` | Retrieve a single room’s status | – | `{status:"success", data:RoomStatusResponse}` |
| `PATCH` | `/rooms/status/{room_id}` | Update a room’s status | `UpdateRoomStatusRequest` | `{status:"success", data:RoomStatusResponse}` |
| `POST` | `/rooms/status/bulk-update` | Bulk‑update multiple rooms | `BulkUpdateRequest` | `{status:"success", data:{"updated":<int>}}` |
| `GET` | `/rooms/status/dashboard` | Dashboard with counts per status | – | `{status:"success", data:DashboardResponse}` |
All routes require the **Admin** role (`app.dependencies.require_roles`).

### Supplies (`/supplies`)
*Stubs are present – endpoints follow the same CRUD pattern as room status.*

### Inventory & Damage
*Currently placeholder routers; ready for future implementation.*
---

## OpenAPI Docs
FastAPI is configured with custom URLs:
- **Swagger UI:** `http://localhost:8082/swagger-ui.html`
- **OpenAPI JSON:** `http://localhost:8082/v3/api-docs`
- **ReDoc (default):** `http://localhost:8082/redoc`
The `app/openapi.py` injects a **Bearer JWT** security scheme globally.
---

## Development Workflow
1. **Branching** – create a short‑lived feature branch off `master`.
2. **Code style** – run `ruff .`, `black .`, and `isort .` before committing.
3. **Pre‑commit hooks** – the repository includes a `.pre-commit-config.yaml` that runs the above automatically.
4. **Commit messages** – use Conventional Commits (`feat:`, `fix:`, `chore:` …).
5. **Pull Requests** – target `master`; CI runs lint, tests, and a Docker build.
---

## Testing
```bash
pip install pytest httpx pytest-asyncio  # already in dev dependencies
pytest
```
Tests cover repository logic (SQLite in‑memory), API layer (FastAPI TestClient with overridden dependencies), and Redis publishing (mocked).
---

## Database Migrations
The project uses **Alembic**.
```bash
# Initialise (run once)
alembic init alembic
# Create a new migration
alembic revision --autogenerate -m "Add room_status table"
# Apply migrations
alembic upgrade head
```
Migrations live under `alembic/versions/`. The Docker image runs `alembic upgrade head` on start‑up (add an entrypoint script if you need custom behaviour).
---

## Logging & Monitoring
- **Logging** – structured JSON logs via the standard `logging` module; level controlled by `LOG_LEVEL`.
- **Metrics** – optional Prometheus exporter (add `starlette_exporter` and include a `/metrics` endpoint).
- **Health checks** – `GET /healthz` (implemented in `app/main.py`) returns `200 OK` when DB and Redis connections are healthy.
---

## Troubleshooting
| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `AsyncSession not defined` | Missing import in router (fixed) | N/A |
| `uvicorn: executable not found` | Docker CMD previously wrong (fixed) | N/A |
| Kafka startup errors | Missing `KAFKA_CONTROLLER_LISTENER_NAMES` (added) | N/A |
| 404 on `/docs` | Docs URL customized (`/swagger-ui.html`) | Use the custom URL or add a redirect (see `app/main.py`). |
| **No operations defined in spec** | OpenAPI generated before routers were registered. | Fixed by moving `custom_openapi(app)` *after* `app.include_router(...)` (see updated `app/main.py`). |
| DB connection refused | Wrong `DB_URL` or Postgres not ready | Wait a few seconds; check `docker compose logs postgres`. |
| Redis timeout | Incorrect `REDIS_URL` port (`6380` host‑side mapping) | Ensure you point to the host‑side port when running locally. |
---

## License
MIT License – feel free to use, modify, and distribute.
---

**Happy coding!** 🎉
If you encounter any further issues, open an issue in the repository or ping the `#hotel-pms` Slack channel.