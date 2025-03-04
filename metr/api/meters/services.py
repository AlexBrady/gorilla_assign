"""Service module for meters endpoints."""

import csv
import io
import json
import logging
from typing import Any, Dict, Optional, Union
from urllib.parse import urlencode

import dicttoxml
from aws_lambda_typing.responses import APIGatewayProxyResponseV2

from metr.core.exceptions import BadRequestException
from metr.database.models import Meter
from metr.api.meters.persistors import MeterPersistor

dicttoxml.LOG.setLevel(logging.ERROR)


class MeterService:
    """Class to hold the logic for handling meters."""

    def __init__(
        self,
        headers: Dict[str, str],
        base_url: str,
        query_params: Dict[str, str],
    ):
        """
        Initialize.

        :param headers: The headers of the request.
        :param base_url: The rawPath of the request.
        :param query_params: The extra query parameters of the request.
        """
        self.query_params = query_params
        self.base_url = base_url
        if headers == {}:
            headers = {"accept": "application/json"}
        self.headers = headers
        self.meter_persistor = MeterPersistor()

    def _assign_next_page_hyperlink(
        self,
        meters_count: int,
        page: int,
        page_size: int,
    ) -> Optional[str]:
        """
        Insert a hyperlink with the next page for pagination.

        :param meters_count: The total mumber of meter objects in the query.
        :param page: The page number of results to show.
        :param page_size: The number of objects per page.

        :return: A hyperlink with the next page of results.
        """
        next_page = None
        if (page * page_size) < meters_count:
            next_query_params = {"page": page + 1, "page_size": page_size}
            next_page = f"{self.base_url}?{urlencode(next_query_params)}"

        return next_page

    def _format_response_data(
        self,
        body: Dict[str, Any],
        content_type: str,
        status_code: int,
    ) -> APIGatewayProxyResponseV2:
        """
        Format the response data based on the Content Type.

        :param body: The body of the request.
        :param content_type: The Content Type to return in the response.
        :param status_code: The status code to return in the response.

        :return: The APIGatewayProxyResponseV2.
        """
        response_data = APIGatewayProxyResponseV2(
            statusCode=status_code,
            headers={"content-type": content_type},
            body=json.dumps(body),
        )

        if content_type == "application/xml":
            response_data["body"] = dicttoxml.dicttoxml(json.dumps(body))
        elif content_type == "text/csv":
            output = io.StringIO()
            csv_writer = csv.DictWriter(output, fieldnames=body["meters"][0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(body["meters"])
            response_data["body"] = output.getvalue()

        return response_data

    def _get_meter_by_id(self, meter_id: int) -> Meter:
        """
        Return a Meter object by its ID.

        :param meter_id: The ID of the Meter.
        :return: The Meter object.
        """
        meter = self.meter_persistor.get_meter(meter_id)
        if not meter:
            raise BadRequestException(f"Meter not found. ID: {meter_id}")

        return meter

    def add_meter(
        self, meter_data: Dict[str, Union[int, bool, float, str]]
    ) -> APIGatewayProxyResponseV2:
        """
        Add a meter to the DB.

        :param meter_data: A dict of the meter data to add.
        :return: The APIGatewayProxyResponseV2 of the new meter.
        """
        meter = Meter(
            external_reference=meter_data["external_reference"],
            supply_start_date=meter_data["supply_start_date"],
            supply_end_date=meter_data["supply_end_date"],
            enabled=bool(meter_data["enabled"]),
            annual_quantity=float(meter_data["annual_quantity"]),
        )

        if self.meter_persistor.does_external_reference_exist(meter.external_reference):
            raise BadRequestException(
                "Meter with this external reference already exists."
            )

        self.meter_persistor.add_meter(meter)

        return self._format_response_data(
            body=meter.as_dict(),
            content_type=self.headers["accept"],
            status_code=201,
        )

    def get_meters(self):
        """
        Get a list of meters.
        """
        meters = self.meter_persistor.get_meters(**self.query_params)
        count_params = {k:v for k,v in self.query_params.items() if k not in ("page", "page_size")}
        meters_count = self.meter_persistor.count_meters(**count_params)

        page, page_size = int(self.query_params.get("page", 1)), int(self.query_params.get("page_size", 20))
        next_page = self._assign_next_page_hyperlink(
            page=page,
            page_size=page_size,
            meters_count=meters_count,
        )
        body = {
            "page": page,
            "page_size": page_size,
            "total": meters_count,
            "meters": [meter.as_dict() for meter in meters],
            "next_page": next_page,
        }

        response_data = self._format_response_data(
            body=body, content_type=self.headers["accept"], status_code=200
        )
        return response_data

    def get_meter(self, path_parameters: Dict[str, str]) -> APIGatewayProxyResponseV2:
        """
        Get a meter by it's PK.

        :param path_parameters: The pathParameters of the request.
        :return: The APIGatewayProxyResponseV2 of the meter.
        """
        meter_id = path_parameters.get("meter_id")
        if not meter_id:
            raise BadRequestException("Meter ID required.")

        meter = self._get_meter_by_id(int(meter_id))
        return self._format_response_data(
            meter.as_dict(), self.headers["accept"], status_code=200
        )

    def update_meter(self, meter_data: Dict[str, Any]) -> APIGatewayProxyResponseV2:
        """
        Update a meter.

        :param meter_data: The data tp update for the meter.
        :return: The APIGatewayProxyResponseV2 with the updated meter.
        """
        meter_id = meter_data.get("meter_id")
        if int(self.base_url.split("/", 2)[2]) != meter_id:
            raise BadRequestException(
                "Meter ID in the body does not match the meter to be updated."
            )
        meter = self._get_meter_by_id(int(meter_id))

        for key, value in meter_data.items():
            if hasattr(meter, key):
                if (
                    key == "external_reference"
                    and self.meter_persistor.does_external_reference_exist(value)
                ):
                    raise BadRequestException(
                        "Meter with this external reference already exists."
                    )
                setattr(meter, key, value)

        self.meter_persistor.update_meter(meter)

        return self._format_response_data(
            body=meter.as_dict(), content_type=self.headers["accept"], status_code=200
        )

    def delete_meter(self, path_parameters: Dict[str, str]):
        """
        Delete a Meter object by its ID.

        :param path_parameters: The pathParameters of the request.
        """
        meter_id = path_parameters.get("meter_id")
        if not meter_id:
            raise BadRequestException("Meter ID required.")

        if not self.meter_persistor.delete_meter(int(meter_id)):
            raise BadRequestException("Meter does not exist.")
