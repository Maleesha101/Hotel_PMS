"""FastAPI application entry point for the Housekeeping & Inventory Service.

"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.database import engine
from app.models import Base
from app.openapi import custom_openapi

from app.domain.room_status.router import router as room_status_router
from app.domain.tasks.router import router as tasks_router
from app.domain.supplies.router import router as supplies_router
from app.domain.inventory.router import router as inventory_router
from app.domain.damage.router import router as damage_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions: ensure DB connection works, start Kafka, scheduler, etc.
    async with engine.begin() as conn:
        # Create tables defined in models if they do not exist
        await conn.run_sync(Base.metadata.create_all)
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

# Include routers under /api/v1 prefix
app.include_router(room_status_router, prefix="/api/v1", tags=["Room Status"])
app.include_router(tasks_router,       prefix="/api/v1", tags=["Housekeeping Tasks"])
app.include_router(supplies_router,    prefix="/api/v1", tags=["Room Supply Standards"])
app.include_router(inventory_router,   prefix="/api/v1", tags=["Inventory"])
app.include_router(damage_router,      prefix="/api/v1", tags=["Damage Reports"])

@app.get("/", tags=["Health Check"])
async def health_check():
    """Base endpoint to verify the service is operational."""
    return {"status": "up", "service": "Housekeeping & Inventory Service"}

# Apply custom OpenAPI (JWT Bearer auth) after all routers are included
custom_openapi(app)
