"""Class to hold custom exceptions."""


class APIException(Exception):
    """Base exception class for API errors."""

    status_code = 500
    default_message = "An unexpected error occurred."

    def __init__(self, message: str = None):
        self.message = message or self.default_message
        super().__init__(self.message)

    def to_dict(self):
        return {"error": self.message, "status_code": self.status_code}


class BadRequestException(APIException):
    """Exception for HTTP 400 Bad Request."""

    status_code = 400
    default_message = "Bad Request."
