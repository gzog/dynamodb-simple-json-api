# Simple Key-Value Store with FastAPI and DynamoDB

This is a simple example of a key-value store built using FastAPI and DynamoDB. All data is stored in a single DynamoDB table.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

1. Python 3.8+
2. AWS CLI configured with appropriate permissions to access DynamoDB
3. FastAPI
4. Uvicorn

### Installation

1. Clone the repository
    ```bash
    git clone https://github.com/yourusername/simple-kv-store.git
    ```

2. Navigate to the project folder
    ```bash
    cd simple-kv-store
    ```

3. Install required Python packages
    ```bash
    pip install -r requirements.txt
    ```

4. Create a DynamoDB table using the AWS CLI
    ```bash
    aws dynamodb create-table \
        --table-name KeyValueTable \
        --attribute-definitions AttributeName=key,AttributeType=S \
        --key-schema AttributeName=key,KeyType=HASH \
        --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
    ```

## Running the API Server

Run the Uvicorn server from the command line:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Open your browser and navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to view the interactive FastAPI documentation.

## Endpoints

- **GET `/items/{key}`**: Retrieve a value by its key.
- **POST `/items/`**: Insert a new key-value pair. The request body should contain a JSON object with `key` and `value` attributes.
- **PUT `/items/{key}`**: Update the value for an existing key. The request body should contain the new `value`.
- **DELETE `/items/{key}`**: Remove a key-value pair by its key.

### Example Usage

1. Insert a new key-value pair
    ```bash
    curl -X 'POST' \
      'http://localhost:8000/items/' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "key": "sample_key",
      "value": "sample_value"
    }'
    ```

2. Retrieve a value by its key
    ```bash
    curl -X 'GET' \
      'http://localhost:8000/items/sample_key' \
      -H 'accept: application/json'
    ```
