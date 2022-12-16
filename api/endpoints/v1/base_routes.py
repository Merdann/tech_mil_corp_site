from endpoints.v1.routes import authentication
from endpoints.v1.routes import follow_us
from endpoints.v1.routes import carousel_about
from endpoints.v1.routes import carousel_main
from endpoints.v1.routes import languages
from endpoints.v1.routes import lets_talk
from endpoints.v1.routes import main_video
from endpoints.v1.routes import projects
from endpoints.v1.routes import users
from fastapi import APIRouter
from fastapi.responses import RedirectResponse


base_router = APIRouter(include_in_schema=False)
api_router = APIRouter(prefix="/api/v1")


@base_router.get("/")
async def default_page():
    return RedirectResponse("/docs")


api_router.include_router(
    authentication.router,
    prefix="/authentication",
    tags=["authentication"],
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)

api_router.include_router(
    languages.router,
    prefix="/languages",
    tags=["languages"],
)

api_router.include_router(
    carousel_main.router,
    prefix="/carousel_main",
    tags=["carousel_main"],
)

api_router.include_router(
    carousel_about.router,
    prefix="/carousel_about",
    tags=["carousel_about"],
)

api_router.include_router(
    projects.router,
    prefix="/projects",
    tags=["projects"],
)

api_router.include_router(
    main_video.router,
    prefix="/main_video",
    tags=["main_video"],
)

api_router.include_router(
    lets_talk.router,
    prefix="/lets_talk",
    tags=["lets_talk"],
)

api_router.include_router(
    follow_us.router,
    prefix="/follow_us",
    tags=["follow_us"],
)
