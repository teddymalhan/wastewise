# Testing Documentation

## Overview

This directory contains comprehensive unit tests for the WasteWise backend application, designed to achieve 100% code coverage using pytest.

## Test Structure

```
backend/test/
├── conftest.py                    # Shared fixtures and test configuration
├── test_main.py                   # Tests for main.py (FastAPI endpoints)
├── test_garbage_controller.py     # Tests for garbage_controller.py
├── test_garbage_model.py          # Tests for garbage_model.py
├── test_faiss_helper.py          # Tests for faiss_helper.py
├── test_langchain_helper.py      # Tests for langchain_helper.py
└── test_embeddings.py            # Tests for embeddings.py
```

## Setup

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

The key testing dependencies are:

- `pytest==8.3.3` - Testing framework
- `pytest-cov==5.0.0` - Coverage plugin
- `pytest-asyncio==0.24.0` - Async testing support
- `pytest-mock==3.14.0` - Enhanced mocking
- `httpx==0.27.2` - FastAPI test client support

## Running Tests

### Run All Tests

```bash
cd backend
pytest
```

### Run Tests with Coverage Report

```bash
pytest --cov=. --cov-report=term-missing --cov-report=html
```

This will:

- Run all tests
- Display coverage report in terminal with missing lines
- Generate an HTML coverage report in `htmlcov/`

### Run Specific Test Files

```bash
# Test only main.py
pytest test/test_main.py

# Test only garbage_model.py
pytest test/test_garbage_model.py
```

### Run Specific Test Functions

```bash
# Run a specific test
pytest test/test_main.py::test_upload_endpoint_success

# Run tests matching a pattern
pytest -k "upload"
```

### Run Tests with Verbose Output

```bash
pytest -v
```

### Run Tests and Stop at First Failure

```bash
pytest -x
```

## Coverage Reports

### Terminal Report

The terminal report shows:

- Total coverage percentage
- Coverage per file
- Lines that are not covered (with `--cov-report=term-missing`)

### HTML Report

Open `htmlcov/index.html` in your browser to see:

- Interactive coverage visualization
- Per-file coverage details
- Highlighted uncovered lines

### XML Report (for CI/CD)

```bash
pytest --cov=. --cov-report=xml
```

## Test Configuration

### pytest.ini

The `pytest.ini` file configures:

- Test discovery patterns
- Coverage settings
- Async mode
- Custom markers

### conftest.py

Shared fixtures include:

- `mock_openai_client` - Mocked OpenAI API client
- `mock_neo4j_driver` - Mocked Neo4j database driver
- `mock_s3_client` - Mocked AWS S3/R2 client
- `mock_faiss_index` - Mocked FAISS index
- `sample_embeddings` - Sample embedding vectors
- `sample_item_names` - Sample item names for testing

## Test Coverage Goals

The test suite aims for **100% code coverage** across all modules:

### Coverage by Module

| Module                | Coverage Target | Key Test Areas                                      |
| --------------------- | --------------- | --------------------------------------------------- |
| main.py               | 100%            | FastAPI endpoints, file uploads, OpenAI integration |
| garbage_controller.py | 100%            | Request validation, classification endpoint         |
| garbage_model.py      | 100%            | Classification logic, Neo4j/LLM fallback            |
| faiss_helper.py       | 100%            | FAISS index operations, similarity search           |
| langchain_helper.py   | 100%            | Embedding generation, LLM integration               |
| embeddings.py         | 100%            | CSV processing, data storage                        |

## Writing New Tests

### Test Naming Convention

- Test files: `test_<module_name>.py`
- Test functions: `test_<functionality>_<scenario>`
- Use descriptive names that explain what is being tested

### Test Structure

```python
@pytest.mark.unit
@patch('module.dependency')
def test_function_name_scenario(mock_dependency):
    """Test description explaining what this test validates."""
    # Arrange
    # ... setup test data and mocks

    # Act
    # ... call the function being tested

    # Assert
    # ... verify the expected behavior
```

### Mocking Best Practices

1. Mock external dependencies (OpenAI, Neo4j, S3)
2. Use `@patch` decorator for module-level mocks
3. Configure mock return values before calling the function
4. Verify mocks were called with expected parameters

### Test Markers

- `@pytest.mark.unit` - Unit tests (fast, isolated)
- `@pytest.mark.integration` - Integration tests (slower, external dependencies)

## Common Testing Patterns

### Testing FastAPI Endpoints

```python
def test_endpoint(test_client):
    response = client.post("/endpoint", json={"key": "value"})
    assert response.status_code == 200
    assert response.json() == expected_result
```

### Testing Async Functions

```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == expected
```

### Testing Error Handling

```python
def test_error_case(mock_dependency):
    mock_dependency.side_effect = Exception("Error message")

    with pytest.raises(HTTPException) as exc_info:
        function_that_should_fail()

    assert "Error message" in str(exc_info.value)
```

## Continuous Integration

### Running Tests in CI/CD

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest --cov=. --cov-report=xml --cov-report=term

# Check coverage threshold (optional)
coverage report --fail-under=95
```

## Troubleshooting

### Import Errors

If you see import errors, ensure you're running pytest from the `backend` directory:

```bash
cd backend
pytest
```

### Mock Issues

If mocks aren't working:

1. Verify the patch target matches the import location
2. Check that mocks are configured before the function is called
3. Use `mock.assert_called_once()` to debug

### Async Test Failures

Ensure `pytest-asyncio` is installed and `asyncio_mode = auto` is set in `pytest.ini`

## Coverage Goals and Metrics

### Current Status

Run `pytest --cov=. --cov-report=term` to see current coverage.

### Minimum Thresholds

- Overall coverage: 95%+
- Per-file coverage: 90%+
- Branch coverage: 85%+

## Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [FastAPI testing guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)
