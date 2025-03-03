"""Get meters endpoint file."""

import json

from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV2
from aws_lambda_typing.responses import APIGatewayProxyResponseV2
from sqlalchemy.orm import Session

from metr.api.meters.exceptions import BadRequestException
from metr.api.meters.services import MeterService
from metr.database import Session as DBSession


def post_meters(
    event: APIGatewayProxyEventV2, context: Context
) -> APIGatewayProxyResponseV2:
    """
    Add a meter object to the database.
    """
    try:
        session: Session = DBSession()
        service = MeterService(
            session=session,
            base_url=event.get("rawPath"),
            headers=event.get("headers", {"accept", "application/json"}),
        )
        meter = service.add_meter(json.loads(event.get("body")))

        return meter

    # TODO: Add exceptions.py file to handle multiple re-usable exceptions
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"error": "Internal Server Error", "message": str(e)}),
        }
    finally:
        session.close()


def get_meters(
    event: APIGatewayProxyEventV2, context: Context
) -> APIGatewayProxyResponseV2:
    """
    Fetch all meters from the database with optional filtering and pagination.
    """
    try:
        session: Session = DBSession()
        service = MeterService(
            session=session,
            query_params=event.get("queryStringParameters"),
            base_url=event.get("rawPath"),
            headers=event.get("headers", {}),
        )
        meters = service.get_meters()

        return meters

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"error": "Internal Server Error", "message": str(e)}),
        }
    finally:
        session.close()


def get_meter(
    event: APIGatewayProxyEventV2, context: Context
) -> APIGatewayProxyResponseV2:
    """
    Fetch a meter object from the database.
    """
    try:
        session: Session = DBSession()
        service = MeterService(
            session=session,
            base_url=event.get("rawPath"),
            headers=event.get("headers", {"accept", "application/json"}),
        )
        meter = service.get_meter(event.get("pathParameters").get("meter_id"))

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
    finally:
        session.close()


def put_meter(
    event: APIGatewayProxyEventV2, context: Context
) -> APIGatewayProxyResponseV2:
    """Update a meter entry partially or fully."""
    try:
        session: Session = DBSession()
        service = MeterService(
            session=session,
            base_url=event.get("rawPath"),
            headers=event.get("headers", {"accept", "application/json"}),
        )

        meter = service.update_meter(
            meter_id=event.get("pathParameters").get("meter_id"),
            meter_data=json.loads(event.get("body")),
        )

        return meter
    except BadRequestException as e:
        return {
            "statusCode": e.status_code,
            "headers": {"content-type": "application/json"},
            "body": json.dumps(e.to_dict()),
        }

    except Exception as e:
        session.rollback()
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error", "message": str(e)}),
        }

    finally:
        session.close()


def delete_meter(
    event: APIGatewayProxyEventV2, context: Context
) -> APIGatewayProxyResponseV2:
    """Update a meter entry partially or fully."""
    try:
        session: Session = DBSession()
        service = MeterService(
            session=session,
            base_url=event.get("rawPath"),
            headers=event.get("headers", {"accept", "application/json"}),
        )

        service.delete_meter(
            meter_id=event.get("pathParameters").get("meter_id"),
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

    finally:
        session.close()
