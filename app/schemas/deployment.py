from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.deployment import Environment


class CreateDeploymentRequest(BaseModel):
    """Validated HTTP contract for registering a deployment candidate."""

    service_name: str = Field(min_length=1, max_length=100)
    version: str = Field(min_length=1, max_length=50)
    environment: Environment

    tests_passed: bool

    # Represented as percentage points:
    # 0.5 means 0.5%, 1.0 means 1%, etc.
    error_rate: float = Field(ge=0.0, le=100.0)


class DeploymentResponse(BaseModel):
    """Public representation returned by the deployment API."""

    id: UUID
    service_name: str
    version: str
    environment: Environment
    tests_passed: bool
    error_rate: float
    created_at: datetime
