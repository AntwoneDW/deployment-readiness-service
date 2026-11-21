from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class Environment(StrEnum):
    """Supported deployment target environments."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass(frozen=True, slots=True)
class DeploymentCandidate:
    """Internal representation of a deployment awaiting evaluation."""

    id: UUID
    service_name: str
    version: str
    environment: Environment
    tests_passed: bool
    error_rate: float
    created_at: datetime
