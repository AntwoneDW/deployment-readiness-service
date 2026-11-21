from fastapi import FastAPI

from app.api.routes.deployments import router as deployments_router

app = FastAPI(
    title="Deployment Readiness Service",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    """Return process health for local/runtime checks."""

    return {"status": "ok"}


app.include_router(deployments_router)
