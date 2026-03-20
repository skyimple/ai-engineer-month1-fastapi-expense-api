"""Global exception handling middleware."""

import traceback
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to catch and handle all unhandled exceptions.

    Returns JSON error responses instead of default HTML error pages.
    """

    async def dispatch(self, request: Request, call_next):
        """Process the request and catch any unhandled exceptions.

        Args:
            request: The incoming HTTP request
            call_next: The next middleware/endpoint in the chain

        Returns:
            JSONResponse with error details or normal response
        """
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            # Log the full traceback for debugging
            traceback.print_exc()

            # Determine status code based on exception type
            status_code = 500
            error_message = "Internal server error"

            if isinstance(exc, ValueError):
                status_code = 400
                error_message = str(exc)
            elif hasattr(exc, "status_code"):
                status_code = exc.status_code

            return JSONResponse(
                status_code=status_code,
                content={
                    "error": error_message,
                    "path": str(request.url),
                    "method": request.method,
                },
            )
