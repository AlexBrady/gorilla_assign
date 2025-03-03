"""Service module for meters endpoints."""

import csv
import io
import json
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

import dicttoxml

from metr.api.meters.enums import ContentTypeEnum
from metr.api.meters.persistors import MeterPersistor
from metr.database import Session


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
    ):
        """Format the response data based on the Content Type."""
        response_data = {
            "statusCode": 200,
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
                "statusCode": 200,
                "headers": {"content-type": "text/csv"},
                "body": output.getvalue(),
            }

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
        meter = self.meter_persistor.get_meter(meter_id)
        if not meter:
            raise Exception

        return self._format_response_data(meter_id, self.headers.get("accept"))
