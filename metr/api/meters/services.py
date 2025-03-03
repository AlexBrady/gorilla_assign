"""Service module for meters endpoints."""

import csv
import io
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

import dicttoxml

from metr.api.meters.enums import ContentTypeEnum
from metr.api.meters.exceptions import BadRequestException
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
        self.headers = headers if headers else {"accept": "application/json"}
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
        body: Union[List[Dict[str, Any]], Dict[str, Any]],
        content_type: ContentTypeEnum,
        status_code: Optional[int] = 200,
    ):
        """Format the response data based on the Content Type."""
        response_data = {
            "statusCode": status_code,
            "headers": {"content-type": "application/json"},
            "body": json.dumps(body),
        }

        if content_type == ContentTypeEnum.xml.value:
            response_data = dicttoxml.dicttoxml(response_data)
        elif content_type == ContentTypeEnum.csv.value:
            output = io.StringIO()
            csv_writer = csv.DictWriter(output, fieldnames=body["meters"][0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(body["meters"])
            response_data = {
                "statusCode": status_code,
                "headers": {"content-type": "text/csv"},
                "body": output.getvalue(),
            }

        return response_data

    def _get_meter_by_id(self, meter_id: int) -> Meter:
        """Return a Meter object by its ID."""
        meter = self.meter_persistor.get_meter(meter_id)
        if not meter:
            raise BadRequestException(f"Meter not found. ID: {meter_id}")

        return meter

    def add_meter(self, meter_data: Dict[str, Union[int, bool, float, str]]):
        """
        Add a meter to the DB.
        """
        required_fields = {
            "meter_id",
            "external_reference",
            "supply_start_date",
            "enabled",
            "annual_quantity",
        }
        if not required_fields.issubset(meter_data.keys()):
            raise BadRequestException(
                f"Missing required fields: {required_fields - set(meter_data.keys())}"
            )

        meter = Meter(
            external_reference=meter_data["external_reference"],
            supply_start_date=datetime.strptime(
                meter_data["supply_start_date"], "%Y-%m-%d"
            ),
            supply_end_date=(
                datetime.strptime(meter_data["supply_end_date"], "%Y-%m-%d")
                if meter_data["supply_end_date"]
                else None
            ),
            enabled=bool(meter_data["enabled"]),
            annual_quantity=float(meter_data["annual_quantity"]),
        )
        self.meter_persistor.add_meter(meter)

        return self._format_response_data(
            body=meter.as_dict(),
            content_type=self.headers.get("accept"),
            status_code=201,
        )

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

        body = {
            "total": meters_count,
            "meters": [meter.as_dict() for meter in meters],
            "next_page": next_page,
        }

        response_data = self._format_response_data(
            body=body, content_type=self.headers.get("accept")
        )

        return response_data

    def get_meter(self, meter_id: int):
        """
        Get a meter by it's PK.
        """
        meter = self._get_meter_by_id(meter_id)
        return self._format_response_data(meter.as_dict(), self.headers.get("accept"))

    def update_meter(
        self, meter_id: int, meter_data: Dict[str, Union[int, bool, float, str]]
    ):
        """
        Update a meter.
        """
        meter_id = meter_data.get("meter_id")
        if int(self.base_url.split("/", 2)[2]) != meter_id:
            raise BadRequestException(
                "Meter ID in the body does not match the meter to be updated."
            )
        meter = self._get_meter_by_id(meter_id)

        # Update only provided fields
        for key, value in meter_data.items():
            if hasattr(meter, key):
                if key in ["supply_start_date", "supply_end_date"] and value:
                    value = datetime.fromisoformat(value)
                setattr(meter, key, value)

        self.meter_persistor.update_meter(meter)

        return self._format_response_data(
            body=meter.as_dict(),
            content_type=self.headers.get("accept"),
        )

    def delete_meter(self, meter_id: str):
        """Delete a Meter object by its ID."""
        if not self.meter_persistor.delete_meter(meter_id):
            raise BadRequestException("Meter does not exist.")
