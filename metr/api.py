from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV2
from aws_lambda_typing.responses import APIGatewayProxyResponseV2


def get_meters(
    event: APIGatewayProxyEventV2, context: Context
) -> APIGatewayProxyResponseV2:
    pass


def post_meters(
    event: APIGatewayProxyEventV2, context: Context
) -> APIGatewayProxyResponseV2:
    pass


def get_meter(
    event: APIGatewayProxyEventV2, context: Context
) -> APIGatewayProxyResponseV2:
    pass


def put_meter(
    event: APIGatewayProxyEventV2, context: Context
) -> APIGatewayProxyResponseV2:
    pass


def delete_meter(
    event: APIGatewayProxyEventV2, context: Context
) -> APIGatewayProxyResponseV2:
    pass
