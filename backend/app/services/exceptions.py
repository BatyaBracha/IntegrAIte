"""Custom exceptions for AI services."""


class AIServiceError(Exception):
    """Base exception for AI service failures."""


class BlueprintNotFoundError(AIServiceError):
    """Raised when the requested bot blueprint does not exist."""


class MissingConfigurationError(AIServiceError):
    """Raised when required environment variables are missing."""
