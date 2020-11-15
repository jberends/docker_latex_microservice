#!/usr/bin/env python

"""

inspiration

* https://github.com/eightBEC/fastapi-ml-skeleton/tree/master/fastapi_skeleton
(APACHE 2.0)
* https://github.com/leosussan/fastapi-gino-arq-uvicorn
(PUBLIC DOMAIN)
"""


from fastapi import FastAPI
from starlette.datastructures import Secret

from app.settings.globals import SENTRY_DSN, APP_NAME, APP_VERSION, DEBUG

if isinstance(SENTRY_DSN, Secret) and SENTRY_DSN.__str__() not in ("None", ""):
    from sentry_sdk import initialize_sentry

    initialize_sentry(dsn=SENTRY_DSN.__str__(), integrations=[])


def get_app() -> FastAPI:
    fast_app = FastAPI(title=APP_NAME, version=APP_VERSION, debug=DEBUG)

    # fast_app.include_router(heartbeat.router, prefix=settings.API_PREFIX)
    # fast_app.include_router(versions.router, prefix=settings.API_PREFIX)

    return fast_app


app = get_app()


#
# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/api/version")
# async def version():
#     """Version of the application."""
#     return dict(version=__version__)
#
#
# @app.get("/")
# async def root():
#     return dict(
#         message="latex_docker_microservice",
#         docs=f"http://localhost:8000{app.docs_url}",
#         redoc=f"http://localhost:8000{app.redoc_url}",
#         version=__version__
#     )
