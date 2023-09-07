aws dynamodb update-item \
    --table-name data \
    --key '{"PK": { "S": "API_KEY#secret" }, "SK": { "S": "API_KEY#secret" } }' \
    --attribute-updates '{"VALUE": { "Value": { "S": "API_KEY#secret" } } }' \
    --endpoint-url http://localhost:8000 \
    --region local
