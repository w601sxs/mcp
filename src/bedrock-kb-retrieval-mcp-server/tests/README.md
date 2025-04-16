# Bedrock Knowledge Base Retrieval MCP Server Tests

This directory contains tests for the Bedrock Knowledge Base Retrieval MCP Server.

## Test Structure

The test suite is organized as follows:

- `conftest.py`: Contains pytest fixtures used across multiple test files
- `test_models.py`: Tests for the data models defined in the server
- `test_clients.py`: Tests for the AWS client creation functions
- `test_discovery.py`: Tests for the knowledge base discovery functionality
- `test_runtime.py`: Tests for the knowledge base querying functionality
- `test_server.py`: Tests for the MCP server endpoints and integration

## Running Tests

You can run the tests using the provided `run_tests.sh` script in the parent directory:

```bash
cd src/bedrock-kb-retrieval-mcp-server
./run_tests.sh
```

This script will:
1. Check for required dependencies and install them if needed
2. Set up the Python path correctly
3. Run the tests using pytest

## Running Tests Manually

If you prefer to run the tests manually, you can use pytest directly:

```bash
cd src/bedrock-kb-retrieval-mcp-server
python -m pytest -xvs tests/
```

To run a specific test file:

```bash
python -m pytest -xvs tests/test_models.py
```

To run a specific test class:

```bash
python -m pytest -xvs tests/test_models.py::TestDataSource
```

To run a specific test method:

```bash
python -m pytest -xvs tests/test_models.py::TestDataSource::test_data_source_creation
```

## Running Tests with Coverage

To run the tests with coverage reporting:

```bash
python -m pytest --cov=awslabs.bedrock_kb_retrieval_mcp_server --cov-report=term-missing tests/
```

To generate an HTML coverage report:

```bash
python -m pytest --cov=awslabs.bedrock_kb_retrieval_mcp_server --cov-report=html tests/
```

## Test Dependencies

The tests require the following Python packages:
- pytest
- pytest-asyncio
- pytest-cov
- boto3
- loguru
- pydantic
- mcp[cli]

These dependencies will be automatically installed by the `run_tests.sh` script if they are missing.
