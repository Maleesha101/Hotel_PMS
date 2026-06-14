"""FastAPI application entry point for the Housekeeping & Inventory Service.

This sets up the FastAPI app, registers routers (currently stubs), and configures
startup/shutdown lifecycles for database, Kafka producer/consumer, and scheduler.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.database import engine
from app.openapi import custom_openapi

# Import placeholder routers (they will be implemented later)
from app.domain.room_status.router import router as room_status_router
from app.domain.tasks.router import router as tasks_router
from app.domain.supplies.router import router as supplies_router
from app.domain.inventory.router import router as inventory_router
from app.domain.damage.router import router as damage_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions: ensure DB connection works, start Kafka, scheduler, etc.
    # For now we simply ensure the engine can be created.
    async with engine.begin() as conn:
        await conn.run_sync(lambda _: None)  # No-op to validate connection
    # TODO: init_producer(), start_consumer(), start_scheduler()
    yield
    # Shutdown actions: close connections, stop background tasks.
    # TODO: close producer/consumer, shutdown scheduler.

app = FastAPI(
    title="Hotel PMS — Housekeeping & Inventory Service",
    description="Manages room status, housekeeping tasks, supplies, inventory, and damage reports.",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/swagger-ui.html",
    openapi_url="/v3/api-docs",
)

# Apply custom OpenAPI (JWT Bearer auth)
# Include routers under /api/v1 prefix
app.include_router(room_status_router, prefix="/api/v1", tags=["Room Status"])
app.include_router(tasks_router,       prefix="/api/v1", tags=["Housekeeping Tasks"])
app.include_router(supplies_router,    prefix="/api/v1", tags=["Room Supply Standards"])
app.include_router(inventory_router,   prefix="/api/v1", tags=["Inventory"])
app.include_router(damage_router,      prefix="/api/v1", tags=["Damage Reports"])

# Apply custom OpenAPI after routers are registered
custom_openapi(app)
