from fastapi import FastAPI

app = FastAPI(
    title="Deployment Readiness Service",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}