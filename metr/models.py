import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from metr.database import Base


class Meter(Base):
    __tablename__ = "meter"

    meter_id: Mapped[int] = mapped_column(primary_key=True)
    external_reference: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    supply_start_date: Mapped[datetime.datetime]
    supply_end_date: Mapped[Optional[datetime.datetime]]
    enabled: Mapped[bool]
    annual_quantity: Mapped[float]

    def as_dict(self):
        """Convert Meter object to a dictionary."""
        return {
            "meter_id": self.meter_id,
            "external_reference": self.external_reference,
            "supply_start_date": self.supply_start_date.isoformat(),
            "supply_end_date": (
                self.supply_end_date.isoformat() if self.supply_end_date else None
            ),
            "enabled": self.enabled,
            "annual_quantity": self.annual_quantity,
        }
