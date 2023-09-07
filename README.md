# Simple Key-Value Store with FastAPI and DynamoDB

This is a simple example of a key-value store built using FastAPI and DynamoDB. All data is stored in a single DynamoDB table using single-table design.

## API Features
1. Store and retrieve JSON data
2. Only authentication by api key is supported
3. Rate limiting by api key to 10 requests per second
4. API upload size limit to 400KB

## DynamoDB Table Structure
|PK|SK|VALUE|
|---|---|---|
|String|String|String|

1. Composite primary key (PK, SK)
2. Partition Key is PK
3. Sort Key is SK
4. Value is always a JSON string

### Record model structure
|PK|SK|VALUE|
|---|---|---|
||String|String|

### API Key model structure
|PK|SK|VALUE|
|---|---|---|
|String|String|String|

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
    git clone https://github.com/gzog/dynamodb-simple-json-api
    ```

2. Navigate to the project folder
    ```bash
    cd dynamodb-simple-json-api
    ```

3. Install required Python packages
    ```bash
    poetry install
    ```

4. Create local DynamoDB table
    ```bash
    ./scripts/create-table.sh
    ```
    
5. Create api key needed to access the API
    ```bash
    ./scripts/create-user.sh
    ```

## Running the API Server

Run the Uvicorn server from the command line:

```bash
./scripts/run.sh
```

Open your browser and navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to view the interactive FastAPI documentation.

## Example Endpoints

- **GET `/records/{key}`**: Retrieve a value by its key.
- **POST `/records/{key}`**: Insert a new key-value pair. The request body should contain a JSON object.
- **PUT `/records/{key}`**: Update the value for an existing key. The request body should contain the new `value`.
- **DELETE `/records/{key}`**: Remove a key-value pair by its key.

### Example Usage

1. Insert a new key-value pair
    ```bash
    curl -X 'POST' \
      'http://localhost:8000/records/' \
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
