"""Custom OpenAPI configuration for FastAPI app."""

from fastapi import FastAPI

def custom_openapi(app: FastAPI):
    """Inject JWT Bearer auth scheme into OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = app.openapi()
    # Add security scheme if not present
    components = openapi_schema.get("components", {})
    security_schemes = components.get("securitySchemes", {})
    if "BearerAuth" not in security_schemes:
        security_schemes["BearerAuth"] = {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    components["securitySchemes"] = security_schemes
    openapi_schema["components"] = components
    # Apply globally
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema
