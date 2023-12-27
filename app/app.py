"""
primary entry point serving fastapi app via uvicorn
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config import Settings, APP_DIR
from routes import router

settings = Settings()


def get_app() -> FastAPI:
    """Create a FastAPI app with the specified settings."""

    app = FastAPI(**settings.fastapi_kwargs)
    app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")
    app.include_router(router)
    return app


app = get_app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, factory=True)
