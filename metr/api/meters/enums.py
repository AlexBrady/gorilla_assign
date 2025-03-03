"""File to hold Enums."""

from enum import Enum


class ContentTypeEnum(Enum):
    """Class to hold the possible data content types to return."""

    json = "application/json"
    xml = "application/xml"
    csv = "text/csv"
