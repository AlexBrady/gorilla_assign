"""Meter persisting operations."""

from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy_utils.functions import sort_query

from metr.database import Session
from metr.models import Meter


class MeterPersistor:
    """Persisting operations for meters."""

    def __init__(self, session: Session):
        """Initliaze."""
        self.session = session

    def add_meter(self, meter: Meter):
        """Add a new Meter to the database."""
        self.session.add(meter)

    def get_meters(
        self,
        meter_id: Optional[int] = None,
        external_reference: Optional[str] = None,
        supply_start_date: Optional[datetime] = None,
        supply_end_date: Optional[datetime] = None,
        enabled: Optional[bool] = None,
        annual_quantity: Optional[float] = None,
        order_by: Optional[str] = None,
        page: Optional[int] = 1,
        page_size: Optional[int] = 20,
    ):
        """Get meters based on given criteria."""
        query = self.session.query(Meter)

        if meter_id is not None:
            query = query.filter(Meter.meter_id == meter_id)

        if external_reference is not None:
            query = query.filter(Meter.external_reference == external_reference)

        if enabled is not None:
            query = query.filter(Meter.enabled == enabled)

        if supply_start_date is not None:
            query = query.filter(Meter.supply_start_date >= Meter.supply_start_date)

        # This might be null - so maybe think about removing
        if supply_end_date is not None:
            query = query.filter(Meter.supply_end_date >= Meter.supply_end_date)

        if annual_quantity is not None:
            query = query.filter(Meter.annual_quantity == annual_quantity)

        if order_by is not None:
            query = sort_query(query, order_by)

        return query.offset((page - 1) * page_size).limit(page_size).all()

    def count_meters(
        self,
        meter_id: Optional[int] = None,
        external_reference: Optional[str] = None,
        supply_start_date: Optional[datetime] = None,
        supply_end_date: Optional[datetime] = None,
        enabled: Optional[bool] = None,
        annual_quantity: Optional[float] = None,
    ):
        """Count meters based on given criteria."""
        query = self.session.query(func.count(Meter.meter_id))

        if meter_id is not None:
            query = query.filter(Meter.meter_id == meter_id)

        if external_reference is not None:
            query = query.filter(Meter.external_reference == external_reference)

        if enabled is not None:
            query = query.filter(Meter.enabled == enabled)

        if supply_start_date is not None:
            query = query.filter(Meter.supply_start_date >= Meter.supply_start_date)

        if supply_end_date is not None:
            query = query.filter(Meter.supply_end_date >= Meter.supply_end_date)

        if annual_quantity is not None:
            query = query.filter(Meter.annual_quantity == annual_quantity)

        return query.scalar()

    def get_meter(self, meter_id: int):
        """Get a Meter object by it's ID."""
        query = self.session.query(Meter).filter_by(meter_id=meter_id)

        return query.first()
