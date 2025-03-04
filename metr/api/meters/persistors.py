"""Meter persisting operations."""

from datetime import datetime
from typing import Dict, List, Optional, Union

from sqlalchemy import func
from sqlalchemy_utils.functions import sort_query

from metr.core.base import BasePersistor
from metr.database.models import Meter


class MeterPersistor(BasePersistor):
    """Persisting operations for meters."""

    def does_external_reference_exist(self, external_reference: str) -> bool:
        """
        Check to see if there is a Meter with a given external reference.

        :param external_reference: The external reference
        :return: True if the external reference already exists.
        """
        return (
            self.session.query(Meter)
            .filter(Meter.external_reference == external_reference)
            .scalar()
            is not None
        )

    def add_meter(self, meter: Meter):
        """
        Add a new Meter to the database.

        :param meter: The Meter object to add
        """
        self.session.add(meter)
        self.commit()

    def get_meters(
        self,
        meter_id: Optional[int] = None,
        external_reference: Optional[str] = None,
        supply_start_date: Optional[datetime] = None,
        supply_end_date: Optional[datetime] = None,
        enabled: Optional[bool] = None,
        annual_quantity: Optional[float] = None,
        order_by: Optional[str] = None,
        page: Optional[str] = "1",
        page_size: Optional[str] = "20",
    ) -> List[Dict[str, Union[str, int, float, bool, datetime]]]:
        """
        Get meters based on given criteria.

        :param meter_id: The ID of the meter.
        :param external_reference: Unique identifier used by the integrators system.
        :param supply_start_date: The date this meter started or will start providing data.
        :param supply_end_date: The date this meter stopped or will stop providing data.
        :param enabled: True if the meter is currently active.
        :param annual_quantity: Best guess or average annual quantity this meter measured or will measure.
        :param order_by: The field to order the query results by.
        :param page: The page number of results to show.
        :param page_size: The number of objects per page.

        :return: A list of meter objects.
        """
        query = self.session.query(Meter)

        if meter_id is not None:
            query = query.filter(Meter.meter_id == meter_id)

        if external_reference is not None:
            query = query.filter(Meter.external_reference == external_reference)

        if enabled is not None:
            query = query.filter(Meter.enabled == enabled)

        if supply_start_date is not None:
            query = query.filter(Meter.supply_start_date >= supply_start_date)

        if supply_end_date is not None:
            query = query.filter(Meter.supply_end_date >= Meter.supply_end_date)

        if annual_quantity is not None:
            query = query.filter(Meter.annual_quantity == annual_quantity)

        if order_by is not None:
            query = sort_query(query, order_by)

        if page and page_size:
            query = query.offset((int(page) - 1) * int(page_size)).limit(int(page_size))

        return query.all()

    def count_meters(
        self,
        meter_id: Optional[int] = None,
        external_reference: Optional[str] = None,
        supply_start_date: Optional[datetime] = None,
        supply_end_date: Optional[datetime] = None,
        enabled: Optional[bool] = None,
        annual_quantity: Optional[float] = None,
    ) -> int:
        """
        Count meters based on given criteria.

        :param meter_id: The ID of the meter.
        :param external_reference: Unique identifier used by the integrators system.
        :param supply_start_date: The date this meter started or will start providing data.
        :param supply_end_date: The date this meter stopped or will stop providing data.
        :param enabled: True if the meter is currently active.
        :param annual_quantity: Best guess or average annual quantity this meter measured or will measure.

        :return: Total count of the Meter objects based on data provided.
        """
        query = self.session.query(func.count(Meter.meter_id))

        if meter_id is not None:
            query = query.filter(Meter.meter_id == meter_id)

        if external_reference is not None:
            query = query.filter(Meter.external_reference == external_reference)

        if enabled is not None:
            query = query.filter(Meter.enabled == enabled)

        if supply_start_date is not None:
            query = query.filter(Meter.supply_start_date >= supply_start_date)

        if supply_end_date is not None:
            query = query.filter(Meter.supply_end_date >= Meter.supply_end_date)

        if annual_quantity is not None:
            query = query.filter(Meter.annual_quantity == annual_quantity)

        return query.scalar()

    def get_meter(self, meter_id: int) -> Meter:
        """
        Get a Meter object by it's ID.

        :param meter_id: The ID of the Meter

        :return: The Meter object.
        """
        query = self.session.query(Meter).filter_by(meter_id=meter_id)

        return query.first()

    def update_meter(self, meter: Meter):
        """
        Update a Meter object.

        :param meter: The Meter object to update.
        """
        self.commit()
        self.session.refresh(meter)

    def delete_meter(self, meter_id: int):
        """
        Delete a Meter object.

        :param meter_id: The ID of the meter.
        """
        count = self.session.query(Meter).filter_by(meter_id=meter_id).delete()
        self.commit()

        return count > 0
