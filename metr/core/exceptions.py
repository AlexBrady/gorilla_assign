"""Module to hold custom exceptions."""


class APIException(Exception):
    """Base exception class for API errors."""

    status_code = 500

    def __init__(self, message: str = "An unexpected error occurred."):
        self.message = message
        super().__init__(self.message)

    def to_dict(self):
        return {"error": self.message, "status_code": self.status_code}


class BadRequestException(APIException):
    """Exception for HTTP 400 Bad Request."""

    status_code = 400
    default_message = "Bad Request."
