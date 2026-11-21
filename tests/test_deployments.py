from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_deployment_repository
from app.main import app
from app.repositories.deployment_repository import DeploymentRepository


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Provide each test with isolated in-memory deployment state."""

    repository = DeploymentRepository()

    # Replace the application's shared repository with a fresh instance.
    # FastAPI will use this dependency anywhere the original is requested.
    app.dependency_overrides[get_deployment_repository] = lambda: repository

    with TestClient(app) as test_client:
        yield test_client

    # Avoid leaking this test's dependency configuration into another test.
    app.dependency_overrides.clear()


def test_create_and_get_deployment(client: TestClient) -> None:
    payload = {
        "service_name": "checkout-api",
        "version": "2.14.0",
        "environment": "production",
        "tests_passed": True,
        "error_rate": 0.35,
    }

    create_response = client.post(
        "/deployments",
        json=payload,
    )

    assert create_response.status_code == 201

    created = create_response.json()

    assert created["service_name"] == "checkout-api"
    assert created["version"] == "2.14.0"
    assert created["environment"] == "production"
    assert created["tests_passed"] is True
    assert created["error_rate"] == 0.35

    deployment_id = created["id"]

    get_response = client.get(f"/deployments/{deployment_id}")

    assert get_response.status_code == 200
    assert get_response.json() == created


def test_get_unknown_deployment_returns_404(
    client: TestClient,
) -> None:
    response = client.get("/deployments/11111111-1111-1111-1111-111111111111")

    assert response.status_code == 404


def test_invalid_environment_is_rejected(
    client: TestClient,
) -> None:
    response = client.post(
        "/deployments",
        json={
            "service_name": "checkout-api",
            "version": "2.14.0",
            "environment": "death-star",
            "tests_passed": True,
            "error_rate": 0.35,
        },
    )

    assert response.status_code == 422


def test_negative_error_rate_is_rejected(
    client: TestClient,
) -> None:
    response = client.post(
        "/deployments",
        json={
            "service_name": "checkout-api",
            "version": "2.14.0",
            "environment": "production",
            "tests_passed": True,
            "error_rate": -1.0,
        },
    )

    assert response.status_code == 422
