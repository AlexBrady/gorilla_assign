"""Test module for meters endpoints."""

import csv
import io
import json
import xml.etree.ElementTree as ET

from metr.api.meters.views import get_meter, get_meters
from tests.factories import generate_api_gateway_proxy_event_v2


def test_get_meters_smoke(db_meters, lambda_context):
    event = generate_api_gateway_proxy_event_v2("GET", "/meters")
    response = get_meters(event, lambda_context)

    assert 200 <= response["statusCode"] < 300
    assert "json" in response["headers"]["content-type"]
    assert json.loads(response["body"])


def test_get_meters_smoke_xml(db_meters, lambda_context):
    event = generate_api_gateway_proxy_event_v2(
        "GET", "/meters", headers={"accept": "application/xml"}
    )
    response = get_meters(event, lambda_context)

    assert ET.fromstring(response)


def test_get_meters_smoke_csv(db_meters, lambda_context):
    event = generate_api_gateway_proxy_event_v2(
        "GET", "/meters", headers={"accept": "text/csv"}
    )
    response = get_meters(event, lambda_context)
    csv_content = response["body"]
    csv_reader = csv.reader(io.StringIO(csv_content))

    rows = list(csv_reader)
    assert len(rows) > 1
    assert "meter_id" in rows[0]


def test_get_meters_smoke_with_filter(db_meters, lambda_context):
    event = generate_api_gateway_proxy_event_v2(
        "GET", "/meters", query_string="enabled=true"
    )
    response = get_meters(event, lambda_context)

    assert 200 <= response["statusCode"] < 300
    assert "json" in response["headers"]["content-type"]

    json_response = json.loads(response["body"])
    assert json_response
    for entry in json_response["meters"]:
        assert entry["enabled"] is True


# Add pagination test with offset, limit, hyperlink actually works


def test_get_meter_smoke(db_meters, lambda_context):
    meter_id = db_meters[0].meter_id

    event = generate_api_gateway_proxy_event_v2(
        "GET", f"/meters/{meter_id}", {"meter_id": str(meter_id)}
    )
    response = get_meter(event, lambda_context)
    assert 200 <= response["statusCode"] < 300
    assert "json" in response["headers"]["content-type"]
    assert json.loads(response["body"])


# def test_get_meter_not_found(fresh_db, lambda_context):
#     meter_id = 999
#     event = generate_api_gateway_proxy_event_v2(
#         "GET", f"/meters/{meter_id}", {"meter_id": str(meter_id)}
#     )
#     response = api.get_meter(event, lambda_context)

#     assert 400 <= response["statusCode"] < 500
#     assert "json" in response["headers"]["content-type"]
#     assert json.loads(response["body"])


# def test_post_meters_smoke(fresh_db, lambda_context):
#     event = generate_api_gateway_proxy_event_v2(
#         "POST",
#         "/meters",
#         body=json.dumps(
#             {
#                 "meter_id": 1,
#                 "external_reference": "123XYZ",
#                 "supply_start_date": "2021-01-01",
#                 "supply_end_date": None,
#                 "enabled": True,
#                 "annual_quantity": 123.45,
#             }
#         ),
#     )
#     response = api.post_meters(event, lambda_context)

#     assert 200 <= response["statusCode"] < 300
#     assert "json" in response["headers"]["content-type"]
#     assert json.loads(response["body"])


# def test_put_meter_smoke(db_meters, lambda_context):
#     meter_id = db_meters[0].meter_id

#     event = generate_api_gateway_proxy_event_v2(
#         "PUT",
#         f"/meters/{meter_id}",
#         body=json.dumps(
#             {
#                 "meter_id": meter_id,
#                 "external_reference": "123XYZ",
#                 "supply_start_date": "2021-01-01",
#                 "supply_end_date": None,
#                 "enabled": True,
#                 "annual_quantity": 123.45,
#             }
#         ),
#     )
#     response = api.put_meter(event, lambda_context)

#     assert 200 <= response["statusCode"] < 300
#     assert "json" in response["headers"]["content-type"]
#     assert json.loads(response["body"])


# def test_put_meter_not_found(fresh_db, lambda_context):
#     meter_id = 999

#     event = generate_api_gateway_proxy_event_v2(
#         "PUT",
#         f"/meters/{meter_id}",
#         body=json.dumps(
#             {
#                 "meter_id": meter_id,
#                 "external_reference": "123XYZ",
#                 "supply_start_date": "2021-01-01",
#                 "supply_end_date": None,
#                 "enabled": True,
#                 "annual_quantity": 123.45,
#             }
#         ),
#     )
#     response = api.put_meter(event, lambda_context)

#     assert 400 <= response["statusCode"] < 500
#     assert "json" in response["headers"]["content-type"]
#     assert json.loads(response["body"])


# def test_delete_meter_smoke(db_meters, lambda_context):
#     meter_id = db_meters[-1].meter_id

#     event = generate_api_gateway_proxy_event_v2(
#         "DELETE", f"/meters/{meter_id}", {"meter_id": str(meter_id)}
#     )
#     response = api.delete_meter(event, lambda_context)

#     assert 200 <= response["statusCode"] < 300


# def test_delete_meter_not_found(fresh_db, lambda_context):
#     meter_id = 999

#     event = generate_api_gateway_proxy_event_v2(
#         "DELETE", f"/meters/{meter_id}", {"meter_id": str(meter_id)}
#     )
#     response = api.delete_meter(event, lambda_context)

#     assert 400 <= response["statusCode"] < 500
