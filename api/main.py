#!/usr/bin/env python3
from pathlib import Path

from core.additional_helpers import create_migrations_dirs
from core.additional_helpers import create_static_dirs
from core.config import settings
from core.database.base.fixtures import create_basic_languages
from core.exceptions.exceptions import CustomResponse
from core.security import AuthStaticFiles
from endpoints.v1.base_routes import api_router
from endpoints.v1.base_routes import base_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_offline import FastAPIOffline
from fastapi_pagination import add_pagination


def include_router(app):
    app.include_router(base_router)
    app.include_router(api_router)


def configure_static(app):
    app.mount(
        "/static/images/users",
        AuthStaticFiles(
            directory=Path(__file__).parent / "static/images/users"
        ),
        name="users",
    )
    app.mount(
        "/static/animations",
        StaticFiles(directory="static/animations"),
        name="animations",
    )
    app.mount(
        "/static/images", StaticFiles(directory="static/images"), name="images"
    )
    app.mount(
        "/static/videos", StaticFiles(directory="static/videos"), name="videos"
    )


def add_middleware(app):
    origins = [i for i in settings.ALLOWED_CORS_ORIGINS.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def adding_pagination(app):
    add_pagination(app)


def start_application():
    app = FastAPIOffline(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        default_response_class=CustomResponse,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
    )
    create_migrations_dirs()
    create_static_dirs()
    configure_static(app)
    include_router(app)
    add_middleware(app)
    adding_pagination(app)
    create_basic_languages()

    return app


app = start_application()


if __name__ == "__main__":
    import subprocess

    command = "gunicorn main:app --bind 0.0.0.0:8000 --workers 3 --threads 2 --worker-class uvicorn.workers.UvicornWorker --access-logfile -"
    subprocess.run(command.split())
