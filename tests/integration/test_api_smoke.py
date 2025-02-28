"""Test module for meters endpoints."""

import json
import xml.etree.ElementTree as ET

from metr.api.meters.views import get_meters
from tests.factories import generate_api_gateway_proxy_event_v2


def test_get_meters_smoke(db_meters, lambda_context):
    event = generate_api_gateway_proxy_event_v2("GET", "/meters")
    resp = get_meters(event, lambda_context)

    print(resp)

    assert 200 <= resp["statusCode"] < 300
    assert "json" in resp["headers"]["content-type"]
    assert json.loads(resp["body"])


def test_get_meters_smoke_xml(db_meters, lambda_context):
    event = generate_api_gateway_proxy_event_v2(
        "GET", "/meters", headers={"accept": "application/xml"}
    )
    resp = get_meters(event, lambda_context)

    assert ET.fromstring(resp)


def test_get_meters_smoke_with_filter(db_meters, lambda_context):
    event = generate_api_gateway_proxy_event_v2(
        "GET", "/meters", query_string="enabled=true"
    )
    resp = get_meters(event, lambda_context)

    assert 200 <= resp["statusCode"] < 300
    assert "json" in resp["headers"]["content-type"]

    json_response = json.loads(resp["body"])
    assert json_response
    for entry in json_response["meters"]:
        assert entry["enabled"] is True


# def test_get_meter_smoke(db_meters, lambda_context):
#     meter_id = db_meters[0].meter_id

#     event = generate_api_gateway_proxy_event_v2(
#         "GET", f"/meters/{meter_id}", {"meter_id": str(meter_id)}
#     )
#     resp = api.get_meter(event, lambda_context)

#     assert 200 <= resp["statusCode"] < 300
#     assert "json" in resp["headers"]["content-type"]
#     assert json.loads(resp["body"])


# def test_get_meter_not_found(fresh_db, lambda_context):
#     meter_id = 999
#     event = generate_api_gateway_proxy_event_v2(
#         "GET", f"/meters/{meter_id}", {"meter_id": str(meter_id)}
#     )
#     resp = api.get_meter(event, lambda_context)

#     assert 400 <= resp["statusCode"] < 500
#     assert "json" in resp["headers"]["content-type"]
#     assert json.loads(resp["body"])


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
#     resp = api.post_meters(event, lambda_context)

#     assert 200 <= resp["statusCode"] < 300
#     assert "json" in resp["headers"]["content-type"]
#     assert json.loads(resp["body"])


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
#     resp = api.put_meter(event, lambda_context)

#     assert 200 <= resp["statusCode"] < 300
#     assert "json" in resp["headers"]["content-type"]
#     assert json.loads(resp["body"])


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
#     resp = api.put_meter(event, lambda_context)

#     assert 400 <= resp["statusCode"] < 500
#     assert "json" in resp["headers"]["content-type"]
#     assert json.loads(resp["body"])


# def test_delete_meter_smoke(db_meters, lambda_context):
#     meter_id = db_meters[-1].meter_id

#     event = generate_api_gateway_proxy_event_v2(
#         "DELETE", f"/meters/{meter_id}", {"meter_id": str(meter_id)}
#     )
#     resp = api.delete_meter(event, lambda_context)

#     assert 200 <= resp["statusCode"] < 300


# def test_delete_meter_not_found(fresh_db, lambda_context):
#     meter_id = 999

#     event = generate_api_gateway_proxy_event_v2(
#         "DELETE", f"/meters/{meter_id}", {"meter_id": str(meter_id)}
#     )
#     resp = api.delete_meter(event, lambda_context)

#     assert 400 <= resp["statusCode"] < 500
