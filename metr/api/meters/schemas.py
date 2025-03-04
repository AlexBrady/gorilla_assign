"""Module to manage schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MeterSchema(BaseModel):
    """Meter Schema"""

    meter_id: int = Field(gt=0)
    external_reference: Optional[str] = None
    supply_start_date: datetime
    supply_end_date: Optional[datetime] = None
    enabled: bool = True
    annual_quantity: float = Field(gt=0)

    class Config:
        from_attributes = True
