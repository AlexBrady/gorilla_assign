"""Get meters endpoint file."""

import json

from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV2
from aws_lambda_typing.responses import APIGatewayProxyResponseV2
from pydantic import ValidationError

from metr.core.exceptions import BadRequestException
from metr.api.meters.schemas import MeterSchema
from metr.api.meters.services import MeterService


def post_meters(
    event: APIGatewayProxyEventV2, context: Context
) -> APIGatewayProxyResponseV2:
    """
    Add a meter object to the database.
    """
    try:
        service = MeterService(
            base_url=event["rawPath"],
            headers=event.get("headers", {"accept": "application/json"}),
            query_params=event.get("queryStringParameters", {}),
        )
        meter = MeterSchema(**json.loads(event["body"]))
        new_meter = service.add_meter(meter.dict())

        return new_meter
    except BadRequestException as e:
        return {
            "statusCode": e.status_code,
            "headers": {"content-type": "application/json"},
            "body": json.dumps(e.to_dict()),
        }
    except ValidationError as e:
        return {
            "statusCode": 400,
            "headers": {"content-type": "application/json"},
            "body": json.dumps(
                {
                    "error": "Bad Request",
                    "message": "Validation failed",
                    "details": e.errors(),
                }
            ),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"error": "Internal Server Error", "message": str(e)}),
        }


def get_meters(
    event: APIGatewayProxyEventV2, context: Context
) -> APIGatewayProxyResponseV2:
    """
    Fetch all meters from the database with optional filtering and pagination.
    """
    try:
        service = MeterService(
            base_url=event["rawPath"],
            headers=event.get("headers", {}),
            query_params=event.get("queryStringParameters", {}),
        )
        meters = service.get_meters()

        return meters

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"error": "Internal Server Error", "message": str(e)}),
        }


def get_meter(
    event: APIGatewayProxyEventV2, context: Context
) -> APIGatewayProxyResponseV2:
    """
    Fetch a meter object from the database.
    """
    try:
        service = MeterService(
            base_url=event["rawPath"],
            headers=event.get("headers", {}),
            query_params=event.get("queryStringParameters", {}),
        )
        meter = service.get_meter(event.get("pathParameters", {}))

        return meter

    except BadRequestException as e:
        return {
            "statusCode": e.status_code,
            "headers": {"content-type": "application/json"},
            "body": json.dumps(e.to_dict()),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"error": "Internal Server Error", "message": str(e)}),
        }


def put_meter(
    event: APIGatewayProxyEventV2, context: Context
) -> APIGatewayProxyResponseV2:
    """Update a meter entry partially or fully."""
    try:
        service = MeterService(
            base_url=event["rawPath"],
            headers=event.get("headers", {}),
            query_params=event.get("queryStringParameters", {}),
        )
        meter = MeterSchema(**json.loads(event.get("body", "")))

        updated_meter = service.update_meter(meter_data=meter.dict())

        return updated_meter
    except BadRequestException as e:
        return {
            "statusCode": e.status_code,
            "headers": {"content-type": "application/json"},
            "body": json.dumps(e.to_dict()),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error", "message": str(e)}),
        }


def delete_meter(
    event: APIGatewayProxyEventV2, context: Context
) -> APIGatewayProxyResponseV2:
    """Update a meter entry partially or fully."""
    try:
        service = MeterService(
            base_url=event["rawPath"],
            headers=event.get("headers", {}),
            query_params=event.get("queryStringParameters", {}),
        )

        service.delete_meter(
            path_parameters=event.get("pathParameters", {}),
        )

        return {"statusCode": 204}

    except BadRequestException as e:
        return {
            "statusCode": e.status_code,
            "headers": {"content-type": "application/json"},
            "body": json.dumps(e.to_dict()),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error", "message": str(e)}),
        }
