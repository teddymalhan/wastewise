"""
Comprehensive unit tests for main.py to achieve 100% code coverage.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch, AsyncMock
from fastapi import UploadFile, HTTPException
from fastapi.testclient import TestClient
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def test_client():
    """Create a test client for FastAPI app."""
    # Mock dependencies before importing main
    with patch('main.s3_client') as mock_s3, \
         patch('main.openai') as mock_openai, \
         patch('model.garbage_model.classify_object') as mock_classify:
        
        # Configure mock classify_object
        mock_classify.return_value = {"object_name": "plastic bottle", "bin_type": "recyclable"}
        
        # Configure mock OpenAI
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock(message=MagicMock(content="plastic bottle"))]
        mock_openai.chat.completions.create.return_value = mock_completion
        
        from main import app
        client = TestClient(app)
        
        yield client, mock_s3, mock_openai, mock_classify


@pytest.mark.unit
def test_upload_endpoint_success(test_client, tmp_path):
    """Test successful file upload and classification."""
    client, mock_s3, mock_openai, mock_classify = test_client
    
    # Create a test image file
    test_file_path = tmp_path / "test_image.jpg"
    test_file_path.write_bytes(b"fake image data")
    
    # Prepare file for upload
    with open(test_file_path, "rb") as f:
        files = {"file": ("test_image.jpg", f, "image/jpeg")}
        response = client.post("/upload/", files=files)
    
    # Assertions
    assert response.status_code == 200
    result = response.json()
    assert "object_name" in result
    assert "bin_type" in result
    assert result["object_name"] == "plastic bottle"
    assert result["bin_type"] == "recyclable"
    
    # Verify mocks were called
    mock_s3.upload_file.assert_called_once()
    mock_openai.chat.completions.create.assert_called_once()
    mock_classify.assert_called_once_with("plastic bottle")


@pytest.mark.unit
def test_upload_endpoint_creates_images_directory(test_client, tmp_path, monkeypatch):
    """Test that images directory is created if it doesn't exist."""
    client, mock_s3, mock_openai, mock_classify = test_client
    
    # Change to temp directory
    monkeypatch.chdir(tmp_path)
    
    # Ensure images directory doesn't exist
    images_dir = tmp_path / "images"
    if images_dir.exists():
        images_dir.rmdir()
    
    # Create a test file
    test_file_path = tmp_path / "test.jpg"
    test_file_path.write_bytes(b"test data")
    
    with open(test_file_path, "rb") as f:
        files = {"file": ("test.jpg", f, "image/jpeg")}
        response = client.post("/upload/", files=files)
    
    # Directory should be created
    assert images_dir.exists()
    assert response.status_code == 200


@pytest.mark.unit
def test_upload_endpoint_openai_error(test_client, tmp_path):
    """Test handling of OpenAI API errors."""
    client, mock_s3, mock_openai, mock_classify = test_client
    
    # Configure OpenAI to raise an exception
    mock_openai.chat.completions.create.side_effect = Exception("OpenAI API Error")
    
    # Create test file
    test_file_path = tmp_path / "test_image.jpg"
    test_file_path.write_bytes(b"fake image data")
    
    with open(test_file_path, "rb") as f:
        files = {"file": ("test_image.jpg", f, "image/jpeg")}
        response = client.post("/upload/", files=files)
    
    # Should return 500 error
    assert response.status_code == 500
    assert "Error in GPT-4 Vision call" in response.json()["detail"]


@pytest.mark.unit
def test_upload_endpoint_s3_upload(test_client, tmp_path):
    """Test that file is uploaded to S3."""
    client, mock_s3, mock_openai, mock_classify = test_client
    
    test_file_path = tmp_path / "upload_test.jpg"
    test_file_path.write_bytes(b"test data")
    
    with open(test_file_path, "rb") as f:
        files = {"file": ("upload_test.jpg", f, "image/jpeg")}
        response = client.post("/upload/", files=files)
    
    # Verify S3 upload was called with correct parameters
    assert response.status_code == 200
    mock_s3.upload_file.assert_called_once()
    call_args = mock_s3.upload_file.call_args
    assert "upload_test.jpg" in call_args[0][0]  # file path
    assert call_args[0][2] == "upload_test.jpg"  # filename


@pytest.mark.unit
def test_upload_endpoint_constructs_correct_image_url(test_client, tmp_path):
    """Test that the correct image URL is constructed for OpenAI."""
    client, mock_s3, mock_openai, mock_classify = test_client
    
    test_file_path = tmp_path / "url_test.jpg"
    test_file_path.write_bytes(b"test")
    
    with open(test_file_path, "rb") as f:
        files = {"file": ("url_test.jpg", f, "image/jpeg")}
        response = client.post("/upload/", files=files)
    
    # Check that OpenAI was called with correct URL structure
    assert response.status_code == 200
    call_args = mock_openai.chat.completions.create.call_args
    messages = call_args[1]["messages"]
    content = messages[0]["content"]
    
    # Find the image URL in the content
    image_url_item = next(item for item in content if item["type"] == "image_url")
    assert "url_test.jpg" in image_url_item["image_url"]["url"]


@pytest.mark.unit
def test_upload_endpoint_file_saved_locally(test_client, tmp_path, monkeypatch):
    """Test that uploaded file is saved locally."""
    client, mock_s3, mock_openai, mock_classify = test_client
    
    monkeypatch.chdir(tmp_path)
    
    test_file_path = tmp_path / "local_save.jpg"
    test_file_path.write_bytes(b"local test data")
    
    with open(test_file_path, "rb") as f:
        files = {"file": ("local_save.jpg", f, "image/jpeg")}
        response = client.post("/upload/", files=files)
    
    # Check file was saved
    saved_file = tmp_path / "images" / "local_save.jpg"
    assert saved_file.exists()
    assert response.status_code == 200


@pytest.mark.unit
def test_upload_endpoint_openai_message_format(test_client, tmp_path):
    """Test that OpenAI receives correctly formatted messages."""
    client, mock_s3, mock_openai, mock_classify = test_client
    
    test_file_path = tmp_path / "format_test.jpg"
    test_file_path.write_bytes(b"test")
    
    with open(test_file_path, "rb") as f:
        files = {"file": ("format_test.jpg", f, "image/jpeg")}
        client.post("/upload/", files=files)
    
    # Verify message format
    call_args = mock_openai.chat.completions.create.call_args
    assert call_args[1]["model"] == "gpt-4o-mini"
    assert call_args[1]["max_tokens"] == 300
    
    messages = call_args[1]["messages"]
    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert len(messages[0]["content"]) == 2
    assert messages[0]["content"][0]["type"] == "text"
    assert messages[0]["content"][1]["type"] == "image_url"


@pytest.mark.unit
def test_cors_middleware_configured():
    """Test that CORS middleware is properly configured."""
    from main import app
    
    # Check middleware is added
    middleware_types = [type(m).__name__ for m in app.user_middleware]
    assert 'CORSMiddleware' in middleware_types


@pytest.mark.unit
def test_environment_variables_loaded():
    """Test that environment variables are loaded."""
    from main import R2_ACCESS_KEY, R2_SECRET_KEY, OPENAI_API_KEY
    
    # These should be set from conftest.py fixture
    assert R2_ACCESS_KEY is not None
    assert R2_SECRET_KEY is not None
    assert OPENAI_API_KEY is not None


@pytest.mark.unit
def test_s3_client_initialized():
    """Test that S3 client is initialized with correct configuration."""
    from main import s3_client, R2_ENDPOINT_URL, R2_REGION
    
    assert s3_client is not None
    # Client should have the endpoint_url configured
    assert hasattr(s3_client, '_endpoint')


@pytest.mark.unit
def test_upload_endpoint_different_file_types(test_client, tmp_path):
    """Test upload with different file types."""
    client, mock_s3, mock_openai, mock_classify = test_client
    
    file_types = [
        ("test.png", "image/png"),
        ("test.jpeg", "image/jpeg"),
        ("test.jpg", "image/jpg"),
    ]
    
    for filename, mime_type in file_types:
        test_file_path = tmp_path / filename
        test_file_path.write_bytes(b"test data")
        
        with open(test_file_path, "rb") as f:
            files = {"file": (filename, f, mime_type)}
            response = client.post("/upload/", files=files)
        
        assert response.status_code == 200


@pytest.mark.unit
def test_upload_endpoint_returns_classification_result(test_client, tmp_path):
    """Test that upload endpoint returns the classification result."""
    client, mock_s3, mock_openai, mock_classify = test_client
    
    # Configure different classification result
    mock_classify.return_value = {"object_name": "banana peel", "bin_type": "compostable"}
    
    test_file_path = tmp_path / "banana.jpg"
    test_file_path.write_bytes(b"banana image")
    
    with open(test_file_path, "rb") as f:
        files = {"file": ("banana.jpg", f, "image/jpeg")}
        response = client.post("/upload/", files=files)
    
    result = response.json()
    assert result["object_name"] == "banana peel"
    assert result["bin_type"] == "compostable"
