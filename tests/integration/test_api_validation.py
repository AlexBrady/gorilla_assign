import json

import pytest

from metr.api.views import post_meters
from tests.factories import generate_api_gateway_proxy_event_v2


@pytest.mark.parametrize(
    "body_change",
    [
        {"meter_id": "StringABC"},
        {"enabled": 100},
        {"supply_start_date": "StringABC"},
        {"annual_quantity": "NaN"},
    ],
)
def test_post_meter_invalid_body(body_change, fresh_db, lambda_context):
    base_body = {
        "meter_id": 1,
        "external_reference": "123XYZ",
        "supply_start_date": "2021-01-01",
        "supply_end_date": None,
        "enabled": True,
        "annual_quantity": 123.45,
    }
    base_body.update(body_change)

    event = generate_api_gateway_proxy_event_v2(
        "POST", "/meters", body=json.dumps(base_body)
    )
    resp = post_meters(event, lambda_context)

    assert 400 <= resp["statusCode"] < 500
    assert "json" in resp["headers"]["content-type"]
    assert json.loads(resp["body"])


def test_post_meter_duplicate_id(db_meters, lambda_context):
    event = generate_api_gateway_proxy_event_v2(
        "POST",
        "/meters",
        body=json.dumps(
            {
                "meter_id": db_meters[0].meter_id,
                "external_reference": "123XYZ",
                "supply_start_date": "2021-01-01",
                "supply_end_date": None,
                "enabled": True,
                "annual_quantity": 123.45,
            }
        ),
    )
    resp = post_meters(event, lambda_context)

    assert 400 <= resp["statusCode"] < 500
    assert "json" in resp["headers"]["content-type"]
    assert json.loads(resp["body"])


def test_post_meter_duplicate_ref(db_meters, lambda_context):
    event = generate_api_gateway_proxy_event_v2(
        "POST",
        "/meters",
        body=json.dumps(
            {
                "meter_id": 999,
                "external_reference": db_meters[0].external_reference,
                "supply_start_date": "2021-01-01",
                "supply_end_date": None,
                "enabled": True,
                "annual_quantity": 123.45,
            }
        ),
    )
    resp = post_meters(event, lambda_context)

    assert 400 <= resp["statusCode"] < 500
    assert "json" in resp["headers"]["content-type"]
    assert json.loads(resp["body"])
