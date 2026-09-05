from typing import Any, Optional
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class NILEException(Exception):
    """Base exception for NILE application errors."""

    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, details: Optional[Any] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details


class DataLoadError(NILEException):
    """Raised when data loading or JSON parsing encounters an error."""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, details=details)


class ServiceNotImplementedError(NILEException):
    """Raised when an invoked service component is not yet implemented."""

    def __init__(self, message: str = "Service functionality is not yet implemented."):
        super().__init__(message=message, status_code=status.HTTP_501_NOT_IMPLEMENTED)


async def nile_exception_handler(request: Request, exc: NILEException) -> JSONResponse:
    """Format known NILE domain exceptions into consistent JSON error responses."""
    content = {
        "status": "error",
        "message": exc.message,
    }
    if exc.details is not None:
        content["details"] = exc.details
    return JSONResponse(status_code=exc.status_code, content=content)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Format request validation errors cleanly."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "message": "Request validation failed",
            "detail": exc.errors(),
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Fallback handler to prevent leaking raw tracebacks on unexpected errors."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "An internal server error occurred",
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all custom exception handlers on the FastAPI application."""
    app.add_exception_handler(NILEException, nile_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
