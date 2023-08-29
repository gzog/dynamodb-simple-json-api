import boto3

from app.settings import Environment, settings

if settings.environment == Environment.Local:
    dynamodb = boto3.client(
        "dynamodb",
        endpoint_url="http://localhost:8000",
        region_name=settings.aws_region_name,
    )
else:
    dynamodb = boto3.client(
        "dynamodb",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region_name,
    )
