aws dynamodb update-item \
    --table-name data \
    --key '{"PK": { "S": "API_KEY#secret" }, "SK": { "S": "API_KEY#secret" } }' \
    --attribute-updates '{"VALUE": { "Value": { "S": "{\"id\": 5, \"name\": \"George\"}" } } }' \
    --endpoint-url http://localhost:8000 \
    --region local
