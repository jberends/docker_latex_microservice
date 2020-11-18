from starlette.datastructures import Secret

from application import app
from routers import heartbeat, versions, pdf
from settings.globals import SENTRY_DSN, API_PREFIX, SENTRY_ENABLED

ROUTERS = (heartbeat.router, versions.router, pdf.router)

for r in ROUTERS:
    app.include_router(r, prefix=API_PREFIX)

if SENTRY_ENABLED and isinstance(SENTRY_DSN, Secret) and SENTRY_DSN.__str__() not in ("None", ""):
    from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

    app = SentryAsgiMiddleware(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8888,
                log_level="info", reload=True)
