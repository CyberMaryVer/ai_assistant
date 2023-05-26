# COMMAND TO RUN FOR DEBUGGING:
# uvicorn fastapi_app.fastapp:app --reload --port 9000 --env-file config.env
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from fastapi_app.core.errors import http_error_handler
from fastapi_app.core.errors import http422_error_handler
from fastapi_app.core.examples import add_examples
from fastapi_app.core.metadata import LOGO
from fastapi_app.routes.api import router as api_router
from fastapi_app.routes.index_routes import router as index_router
from fastapi_app.routes.admin import router as admin_router
from fastapi_app.routes.user import router as user_router
from fastapi_app.core.config import get_app_settings
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

from fastapi_app.core.events import create_start_app_handler, create_stop_app_handler
from fastapi_app.config.app_config import DEBUG


def custom_openapi():
    # cache the generated schema
    if app.openapi_schema:
        return app.openapi_schema

    # custom settings
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
    )
    # setting new logo to docs
    openapi_schema["info"]["x-logo"]['url'] = LOGO

    # app.openapi_schema = openapi_schema
    app.openapi_schema = add_examples(openapi_schema, './fastapi_app/examples')

    return app.openapi_schema


def custom_ui_params(config):
    swagger_ui_default_parameters = {
        "dom_id": "#swagger-ui",
        "layout": "BaseLayout",
        "deepLinking": True,
        "showExtensions": True,
        "showCommonExtensions": True,
    }
    for k, v in config.items():
        if k in swagger_ui_default_parameters:
            swagger_ui_default_parameters[k] = v

    return swagger_ui_default_parameters


def get_application() -> FastAPI:
    settings = get_app_settings()

    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # WHEN DATABASE IS READY
    if not DEBUG:
        application.add_event_handler(
            "startup",
            create_start_app_handler(application, settings),
        )
        application.add_event_handler(
            "shutdown",
            create_stop_app_handler(application),
        )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix=settings.api_prefix)
    application.include_router(index_router)
    application.include_router(admin_router, prefix=settings.admin_prefix)
    application.include_router(user_router, prefix="/user")
    application.mount("/static", StaticFiles(directory="./fastapi_app/static"), name="static")

    # application.openapi = custom_openapi
    application.swagger_ui_parameters = custom_ui_params({'showCommonExtensions': False,
                                                          'showExtensions': False})

    # instrument application
    Instrumentator().instrument(application).expose(application)

    return application


app = get_application()