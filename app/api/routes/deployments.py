from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_deployment_service
from app.schemas.deployment import (
    CreateDeploymentRequest,
    DeploymentResponse,
)
from app.services.deployment_service import (
    DeploymentNotFoundError,
    DeploymentService,
)

router = APIRouter(
    prefix="/deployments",
    tags=["deployments"],
)


@router.post(
    "",
    response_model=DeploymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_deployment(
    request: CreateDeploymentRequest,
    service: Annotated[
        DeploymentService,
        Depends(get_deployment_service),
    ],
) -> DeploymentResponse:
    """Register a deployment candidate for readiness evaluation."""

    deployment = service.create(request)

    # Pydantic can construct the response explicitly from our domain object.
    return DeploymentResponse(
        id=deployment.id,
        service_name=deployment.service_name,
        version=deployment.version,
        environment=deployment.environment,
        tests_passed=deployment.tests_passed,
        error_rate=deployment.error_rate,
        created_at=deployment.created_at,
    )


@router.get(
    "/{deployment_id}",
    response_model=DeploymentResponse,
)
def get_deployment(
    deployment_id: UUID,
    service: Annotated[
        DeploymentService,
        Depends(get_deployment_service),
    ],
) -> DeploymentResponse:
    """Retrieve a previously registered deployment candidate."""

    try:
        deployment = service.get(deployment_id)

    except DeploymentNotFoundError as exc:
        # Translate the application error into an HTTP-specific response here.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return DeploymentResponse(
        id=deployment.id,
        service_name=deployment.service_name,
        version=deployment.version,
        environment=deployment.environment,
        tests_passed=deployment.tests_passed,
        error_rate=deployment.error_rate,
        created_at=deployment.created_at,
    )
