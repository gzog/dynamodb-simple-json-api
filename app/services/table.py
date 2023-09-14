from app.utils.aws import get_dynamodb_client
from app.settings import settings
from app.utils.logger import logger


async def create_dynamodb_table() -> None:
    table_name = settings.aws_dynamodb_table_name
    async with get_dynamodb_client() as dynamodb:
        logger.debug("Requesting table creation...")
        await dynamodb.create_table(
            TableName=table_name,
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
        )

        logger.debug("Waiting for table to be created...")
        waiter = dynamodb.get_waiter("table_exists")
        await waiter.wait(TableName=table_name)
        logger.debug(f"Table {table_name} created")
