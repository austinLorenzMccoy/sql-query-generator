from fastapi import FastAPI
from .api.v1.routes import router as api_router
from .core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="Text-to-SQL Backend", version="1.0.0")
    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
