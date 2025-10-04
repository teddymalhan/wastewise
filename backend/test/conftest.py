"""
Pytest configuration and shared fixtures for all tests.
"""
import pytest
import os
import numpy as np
from unittest.mock import Mock, MagicMock, patch
from io import BytesIO


@pytest.fixture(autouse=True)
def setup_env_vars(monkeypatch):
    """Set up environment variables for testing."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
    monkeypatch.setenv("R2_ACCESS_KEY", "test-r2-access-key")
    monkeypatch.setenv("R2_SECRET_KEY", "test-r2-secret-key")


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client."""
    mock_client = MagicMock()
    
    # Mock chat completions
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock(message=MagicMock(content="plastic bottle"))]
    mock_client.chat.completions.create.return_value = mock_completion
    
    # Mock embeddings
    mock_embedding = MagicMock()
    mock_embedding.data = [MagicMock(embedding=[0.1] * 1536)]
    mock_client.embeddings.create.return_value = mock_embedding
    
    return mock_client


@pytest.fixture
def mock_openai_module(mock_openai_client):
    """Mock the openai module."""
    with patch('openai.OpenAI', return_value=mock_openai_client):
        with patch('openai.embeddings.create', return_value=mock_openai_client.embeddings.create.return_value):
            yield mock_openai_client


@pytest.fixture
def mock_neo4j_driver():
    """Mock Neo4j driver."""
    mock_driver = MagicMock()
    mock_session = MagicMock()
    mock_result = MagicMock()
    
    # Default behavior - no records found
    mock_result.single.return_value = None
    mock_result.__iter__.return_value = iter([])
    mock_session.run.return_value = mock_result
    mock_driver.session.return_value.__enter__.return_value = mock_session
    mock_driver.session.return_value.__exit__.return_value = None
    
    return mock_driver


@pytest.fixture
def mock_neo4j_with_data():
    """Mock Neo4j driver with sample data."""
    mock_driver = MagicMock()
    mock_session = MagicMock()
    mock_result = MagicMock()
    
    # Mock data
    mock_record = MagicMock()
    mock_record.__getitem__ = lambda self, key: "recyclable" if key == "bin_type" else "plastic bottle"
    mock_record.get.return_value = "recyclable"
    mock_record.__contains__ = lambda self, key: True
    
    mock_result.single.return_value = mock_record
    mock_result.__iter__.return_value = iter([mock_record])
    mock_session.run.return_value = mock_result
    mock_driver.session.return_value.__enter__.return_value = mock_session
    mock_driver.session.return_value.__exit__.return_value = None
    
    return mock_driver


@pytest.fixture
def mock_s3_client():
    """Mock boto3 S3 client."""
    mock_client = MagicMock()
    mock_client.upload_file.return_value = None
    return mock_client


@pytest.fixture
def mock_faiss_index():
    """Mock FAISS index."""
    mock_index = MagicMock()
    mock_index.d = 1536
    mock_index.ntotal = 100
    mock_index.search.return_value = (
        np.array([[0.1, 0.2, 0.3, 0.4, 0.5]]),
        np.array([[0, 1, 2, 3, 4]])
    )
    return mock_index


@pytest.fixture
def sample_embeddings():
    """Sample embeddings for testing."""
    return np.random.rand(10, 1536).astype('float32')


@pytest.fixture
def sample_item_names():
    """Sample item names for testing."""
    return ['plastic bottle', 'glass jar', 'paper bag', 'aluminum can', 'cardboard box',
            'styrofoam cup', 'banana peel', 'milk carton', 'newspaper', 'tin can']


@pytest.fixture
def mock_uploaded_file():
    """Mock uploaded file for FastAPI."""
    mock_file = MagicMock()
    mock_file.filename = "test_image.jpg"
    mock_file.read.return_value = b"fake image data"
    return mock_file


@pytest.fixture
def mock_csv_file(tmp_path):
    """Create a temporary CSV file for testing."""
    csv_path = tmp_path / "test_data.csv"
    csv_content = """item_name,bin_type
plastic bottle,recyclable
banana peel,compostable
paper bag,recyclable
"""
    csv_path.write_text(csv_content)
    return str(csv_path)
