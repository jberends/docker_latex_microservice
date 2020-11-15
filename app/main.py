import sys


from starlette.datastructures import Secret

from app.application import app
from app.routers import heartbeat, versions
from app.settings.globals import SENTRY_DSN, API_PREFIX

sys.path.extend(["./"])

ROUTERS = (heartbeat.router, versions.router)

for r in ROUTERS:
    app.include_router(r, prefix=API_PREFIX)

if isinstance(SENTRY_DSN, Secret) and SENTRY_DSN.__str__() not in ("None", ""):
    from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

    app.add_middleware(SentryAsgiMiddleware)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8888, log_level="info")
