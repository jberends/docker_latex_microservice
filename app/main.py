#!/usr/bin/env python
"""
This script is part of package `kems_pdf_generator`"""
from fastapi import FastAPI

from __about__ import __version__
from common import APP_NAME, API_PREFIX


def APP_VERSION(args):
    pass


def get_app() -> FastAPI:
    fast_app = FastAPI(title=APP_NAME, version=__version__, debug=DEBUG)
    fast_app.include_router(api_router, prefix=API_PREFIX)

    fast_app.add_event_handler("startup", start_app_handler(fast_app))
    fast_app.add_event_handler("shutdown", stop_app_handler(fast_app))

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
