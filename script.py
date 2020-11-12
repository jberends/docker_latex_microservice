#!/usr/bin/env python
"""
This script is part of package `kems_pdf_generator`"""

__version__ = '0.0.1'

from fastapi import FastAPI

app = FastAPI()


@app.get("/version")
async def version():
    """Version of the application."""
    return dict(version=__version__)

@app.get("/")
async def root():
    return {"message": "Hello World"}
