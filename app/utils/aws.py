from aiobotocore.session import get_session, ClientCreatorContext

from app.settings import Environment, settings


session = get_session()


def get_dynamodb_client() -> ClientCreatorContext:
    if settings.environment == Environment.Production:
        return session.create_client(
            "dynamodb",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region_name,
        )
    else:
        return session.create_client(
            "dynamodb",
            endpoint_url="http://localhost:8000",
            region_name=settings.aws_region_name,
        )
