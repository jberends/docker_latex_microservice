#!/usr/bin/env python

"""

inspiration

* https://github.com/eightBEC/fastapi-ml-skeleton/tree/master/fastapi_skeleton
(APACHE 2.0)
"""


from fastapi import FastAPI

from routers import heartbeat, versions
from __about__ import __version__
from config import settings


def get_app() -> FastAPI:
    fast_app = FastAPI(
        title=settings.APP_NAME, version=__version__, debug=settings.DEBUG
    )

    fast_app.include_router(heartbeat.router, prefix=settings.API_PREFIX)
    fast_app.include_router(versions.router, prefix=settings.API_PREFIX)

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
