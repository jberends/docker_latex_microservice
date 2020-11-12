#!/usr/bin/env python
"""
This script is part of package `kems_pdf_generator`"""

__version__ = '0.0.1'

from fastapi import FastAPI

app = FastAPI()


@app.get("/api/version")
async def version():
    """Version of the application."""
    return dict(version=__version__)


@app.get("/")
async def root():
    return dict(
        message="latex_docker_microservice",
        docs=f"https://localhost:8000{app.docs_url}",
        redoc=f"https://localhost:8000{app.redoc_url}"
    )
