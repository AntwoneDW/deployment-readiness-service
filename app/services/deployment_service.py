from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.models.deployment import DeploymentCandidate
from app.repositories.deployment_repository import DeploymentRepository
from app.schemas.deployment import CreateDeploymentRequest


class DeploymentNotFoundError(Exception):
    """Raised when a requested deployment candidate does not exist."""


class DeploymentService:
    """Coordinates deployment registration and retrieval."""

    def __init__(self, repository: DeploymentRepository) -> None:
        self._repository = repository

    def create(self, request: CreateDeploymentRequest) -> DeploymentCandidate:
        """Create and persist a new deployment candidate."""

        deployment = DeploymentCandidate(
            id=uuid4(),
            service_name=request.service_name,
            version=request.version,
            environment=request.environment,
            tests_passed=request.tests_passed,
            error_rate=request.error_rate,
            created_at=datetime.now(UTC),
        )

        return self._repository.save(deployment)

    def get(self, deployment_id: UUID) -> DeploymentCandidate:
        """Retrieve a deployment or raise a domain-facing not-found error."""

        deployment = self._repository.get_by_id(deployment_id)

        if deployment is None:
            raise DeploymentNotFoundError(
                f"Deployment '{deployment_id}' was not found."
            )

        return deployment
