"""
Comprehensive unit tests for controller/garbage_controller.py to achieve 100% code coverage.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch, AsyncMock
from fastapi import HTTPException
from fastapi.testclient import TestClient
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def test_client_controller():
    """Create a test client for the garbage controller router."""
    with patch('controller.garbage_controller.classify_object') as mock_classify:
        mock_classify.return_value = {"object_name": "plastic bottle", "bin_type": "recyclable"}
        
        from fastapi import FastAPI
        from controller.garbage_controller import router
        
        app = FastAPI()
        app.include_router(router)
        
        client = TestClient(app)
        yield client, mock_classify


@pytest.mark.unit
def test_classify_endpoint_success(test_client_controller):
    """Test successful classification with valid request."""
    client, mock_classify = test_client_controller
    
    request_data = {
        "object_name": "plastic bottle",
        "probability": 0.95
    }
    
    response = client.post("/classify", json=request_data)
    
    assert response.status_code == 200
    result = response.json()
    assert result["object_name"] == "plastic bottle"
    assert result["bin_type"] == "recyclable"
    
    # Verify classify_object was called
    mock_classify.assert_called_once_with("plastic bottle")


@pytest.mark.unit
def test_classify_endpoint_minimum_probability(test_client_controller):
    """Test classification with minimum valid probability (0.5)."""
    client, mock_classify = test_client_controller
    
    request_data = {
        "object_name": "glass jar",
        "probability": 0.5
    }
    
    response = client.post("/classify", json=request_data)
    
    assert response.status_code == 200
    mock_classify.assert_called_once_with("glass jar")


@pytest.mark.unit
def test_classify_endpoint_high_probability(test_client_controller):
    """Test classification with high probability."""
    client, mock_classify = test_client_controller
    
    request_data = {
        "object_name": "banana peel",
        "probability": 0.99
    }
    
    response = client.post("/classify", json=request_data)
    
    assert response.status_code == 200
    mock_classify.assert_called_once_with("banana peel")


@pytest.mark.unit
def test_classify_endpoint_probability_below_threshold(test_client_controller):
    """Test classification with probability below 0.5 threshold."""
    client, mock_classify = test_client_controller
    
    request_data = {
        "object_name": "unknown object",
        "probability": 0.49
    }
    
    response = client.post("/classify", json=request_data)
    
    assert response.status_code == 400
    assert "Probability must be at least 0.5" in response.json()["detail"]
    
    # classify_object should not be called
    mock_classify.assert_not_called()


@pytest.mark.unit
def test_classify_endpoint_very_low_probability(test_client_controller):
    """Test classification with very low probability."""
    client, mock_classify = test_client_controller
    
    request_data = {
        "object_name": "mystery item",
        "probability": 0.1
    }
    
    response = client.post("/classify", json=request_data)
    
    assert response.status_code == 400
    assert "Probability must be at least 0.5" in response.json()["detail"]


@pytest.mark.unit
def test_classify_endpoint_zero_probability(test_client_controller):
    """Test classification with zero probability."""
    client, mock_classify = test_client_controller
    
    request_data = {
        "object_name": "item",
        "probability": 0.0
    }
    
    response = client.post("/classify", json=request_data)
    
    assert response.status_code == 400


@pytest.mark.unit
def test_classify_endpoint_empty_object_name(test_client_controller):
    """Test classification with empty object name."""
    client, mock_classify = test_client_controller
    
    request_data = {
        "object_name": "",
        "probability": 0.8
    }
    
    response = client.post("/classify", json=request_data)
    
    assert response.status_code == 400
    assert "Invalid Request" in response.json()["detail"]


@pytest.mark.unit
def test_classify_endpoint_none_object_name(test_client_controller):
    """Test classification with None as object name - should fail validation."""
    client, mock_classify = test_client_controller
    
    request_data = {
        "object_name": None,
        "probability": 0.8
    }
    
    response = client.post("/classify", json=request_data)
    
    # Pydantic validation should fail
    assert response.status_code == 422


@pytest.mark.unit
def test_classify_endpoint_missing_object_name(test_client_controller):
    """Test classification with missing object_name field."""
    client, mock_classify = test_client_controller
    
    request_data = {
        "probability": 0.8
    }
    
    response = client.post("/classify", json=request_data)
    
    # Pydantic validation should fail
    assert response.status_code == 422


@pytest.mark.unit
def test_classify_endpoint_missing_probability(test_client_controller):
    """Test classification with missing probability field."""
    client, mock_classify = test_client_controller
    
    request_data = {
        "object_name": "test item"
    }
    
    response = client.post("/classify", json=request_data)
    
    # Pydantic validation should fail
    assert response.status_code == 422


@pytest.mark.unit
def test_classify_endpoint_invalid_probability_type(test_client_controller):
    """Test classification with invalid probability type."""
    client, mock_classify = test_client_controller
    
    request_data = {
        "object_name": "test item",
        "probability": "not a number"
    }
    
    response = client.post("/classify", json=request_data)
    
    # Pydantic validation should fail
    assert response.status_code == 422


@pytest.mark.unit
def test_classify_endpoint_negative_probability(test_client_controller):
    """Test classification with negative probability."""
    client, mock_classify = test_client_controller
    
    request_data = {
        "object_name": "test item",
        "probability": -0.5
    }
    
    response = client.post("/classify", json=request_data)
    
    assert response.status_code == 400


@pytest.mark.unit
def test_classify_endpoint_various_bin_types(test_client_controller):
    """Test classification returns different bin types."""
    client, mock_classify = test_client_controller
    
    bin_types = [
        ("recyclable", "plastic bottle"),
        ("compostable", "banana peel"),
        ("garbage", "styrofoam"),
        ("mixed-paper", "newspaper"),
    ]
    
    for expected_bin, item_name in bin_types:
        mock_classify.return_value = {"object_name": item_name, "bin_type": expected_bin}
        
        request_data = {
            "object_name": item_name,
            "probability": 0.9
        }
        
        response = client.post("/classify", json=request_data)
        
        assert response.status_code == 200
        result = response.json()
        assert result["bin_type"] == expected_bin


@pytest.mark.unit
def test_classify_endpoint_special_characters_in_name(test_client_controller):
    """Test classification with special characters in object name."""
    client, mock_classify = test_client_controller
    
    request_data = {
        "object_name": "plastic bottle (16 oz.)",
        "probability": 0.85
    }
    
    response = client.post("/classify", json=request_data)
    
    assert response.status_code == 200
    mock_classify.assert_called_once_with("plastic bottle (16 oz.)")


@pytest.mark.unit
def test_classify_endpoint_long_object_name(test_client_controller):
    """Test classification with very long object name."""
    client, mock_classify = test_client_controller
    
    long_name = "a" * 1000
    request_data = {
        "object_name": long_name,
        "probability": 0.75
    }
    
    response = client.post("/classify", json=request_data)
    
    assert response.status_code == 200
    mock_classify.assert_called_once_with(long_name)


@pytest.mark.unit
def test_garbage_request_model():
    """Test GarbageRequest Pydantic model."""
    from controller.garbage_controller import GarbageRequest
    
    # Valid request
    valid_request = GarbageRequest(object_name="test", probability=0.8)
    assert valid_request.object_name == "test"
    assert valid_request.probability == 0.8
    
    # Test with exactly 0.5
    edge_request = GarbageRequest(object_name="edge", probability=0.5)
    assert edge_request.probability == 0.5


@pytest.mark.unit
def test_classify_endpoint_exact_probability_boundary(test_client_controller):
    """Test classification at exact probability boundaries."""
    client, mock_classify = test_client_controller
    
    # Test 0.5 (should pass)
    response = client.post("/classify", json={"object_name": "item", "probability": 0.5})
    assert response.status_code == 200
    
    # Test 0.4999999 (should fail)
    response = client.post("/classify", json={"object_name": "item", "probability": 0.4999999})
    assert response.status_code == 400
    
    # Test 0.5000001 (should pass)
    response = client.post("/classify", json={"object_name": "item", "probability": 0.5000001})
    assert response.status_code == 200
