from sqlalchemy import Boolean, Column, Date, Float, Integer, String

from metr.database import Base


class Meter(Base):
    __tablename__ = "meter"

    meter_id = Column(Integer, nullable=False, primary_key=True)
    external_reference = Column(String(32), unique=True, index=True)
    supply_start_date = Column(Date, nullable=False)
    supply_end_date = Column(Date)
    enabled = Column(Boolean, nullable=False)
    annual_quantity = Column(Float)
