"""Service module for meters endpoints."""

import json
from typing import Dict, List, Optional, Union
from urllib.parse import urlencode

import dicttoxml

from metr.api.meters.persistors import MeterPersistor
from metr.database import Session
from metr.models import Meter


class MeterService:
    """Class to hold the logic for handling meters."""

    def __init__(
        self,
        session: Session,
        query_params: Optional[Dict[str, Union[int, bool, str, int]]] = None,
        base_url: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """Initialize."""
        self.query_params = query_params
        self.base_url = base_url
        self.headers = headers
        self.meter_persistor = MeterPersistor(session)

    def _assign_next_page_hyperlink(
        self,
        meters_count: int,
        page: int,
        page_size: int,
    ) -> Optional[str]:
        """Insert a hyperlink with the next page for pagination."""
        next_page = None
        if (page * page_size) < meters_count:
            next_query_params = {"page": page + 1, "page_size": page_size}
            next_page = f"{self.base_url}?{urlencode(next_query_params)}"

        return next_page

    def _format_response_data(
        self,
        meters: List[Meter],
        meters_count: int,
        next_page: Optional[str] = None,
    ):
        """Serialize the DB Objects for JSON use."""
        meters_data = [
            {
                "meter_id": meter.meter_id,
                "external_reference": meter.external_reference,
                "supply_start_date": meter.supply_start_date.isoformat(),
                "supply_end_date": (
                    meter.supply_end_date.isoformat() if meter.supply_end_date else None
                ),
                "enabled": meter.enabled,
                "annual_quantity": meter.annual_quantity,
            }
            for meter in meters
        ]

        response_data = {
            "statusCode": 200,
            "headers": {"content-type": "application/json"},
            "body": json.dumps(
                {
                    "total": meters_count,
                    "meters": meters_data,
                    "next_page": next_page,
                }
            ),
        }

        if "xml" in self.headers.get("accept", "application/json").lower():
            response_data = dicttoxml.dicttoxml(response_data)

        return response_data

    def get_meters(self):
        """
        Get a list of meters.
        """
        meters = self.meter_persistor.get_meters(**self.query_params)
        meters_count = self.meter_persistor.count_meters(**self.query_params)
        next_page = self._assign_next_page_hyperlink(
            page=self.query_params.get("page", 1),
            page_size=self.query_params.get("page_size", 20),
            meters_count=meters_count,
        )

        response_data = self._format_response_data(
            meters=meters, meters_count=meters_count, next_page=next_page
        )

        return response_data
