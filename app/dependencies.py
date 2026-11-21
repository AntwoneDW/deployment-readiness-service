from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.repositories.deployment_repository import DeploymentRepository
from app.services.deployment_service import DeploymentService


@lru_cache
def get_deployment_repository() -> DeploymentRepository:
    """Provide the process-wide repository used by the running application."""

    return DeploymentRepository()


def get_deployment_service(
    repository: Annotated[
        DeploymentRepository,
        Depends(get_deployment_repository),
    ],
) -> DeploymentService:
    """Build the application service around the configured repository."""

    return DeploymentService(repository)
