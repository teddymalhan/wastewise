"""
Comprehensive unit tests for model/garbage_model.py to achieve 100% code coverage.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.unit
@patch('model.garbage_model.generate_guess')
@patch('model.garbage_model.retrieve_bin_for_object')
def test_classify_object_neo4j_hit(mock_retrieve, mock_generate):
    """Test classify_object when Neo4j has the object."""
    from model.garbage_model import classify_object
    
    # Mock Neo4j returning a bin type
    mock_retrieve.return_value = "recyclable"
    mock_generate.return_value = "should not be called"
    
    result = classify_object("plastic bottle")
    
    assert result == {"object_name": "plastic bottle", "bin_type": "recyclable"}
    mock_retrieve.assert_called_once_with("plastic bottle")
    # generate_guess should not be called when Neo4j has the data
    mock_generate.assert_not_called()


@pytest.mark.unit
@patch('model.garbage_model.generate_guess')
@patch('model.garbage_model.retrieve_bin_for_object')
def test_classify_object_neo4j_miss_uses_llm(mock_retrieve, mock_generate):
    """Test classify_object falls back to LLM when Neo4j doesn't have the object."""
    from model.garbage_model import classify_object
    
    # Mock Neo4j returning None
    mock_retrieve.return_value = None
    mock_generate.return_value = "compostable"
    
    result = classify_object("banana peel")
    
    assert result == {"object_name": "banana peel", "bin_type": "compostable"}
    mock_retrieve.assert_called_once_with("banana peel")
    mock_generate.assert_called_once_with("banana peel")


@pytest.mark.unit
@patch('model.garbage_model.generate_guess')
@patch('model.garbage_model.retrieve_bin_for_object')
def test_classify_object_neo4j_returns_none_string(mock_retrieve, mock_generate):
    """Test classify_object falls back to LLM when Neo4j returns 'None' as string."""
    from model.garbage_model import classify_object
    
    # Mock Neo4j returning "None" as string
    mock_retrieve.return_value = "None"
    mock_generate.return_value = "garbage"
    
    result = classify_object("styrofoam cup")
    
    assert result == {"object_name": "styrofoam cup", "bin_type": "garbage"}
    mock_retrieve.assert_called_once_with("styrofoam cup")
    mock_generate.assert_called_once_with("styrofoam cup")


@pytest.mark.unit
@patch('model.garbage_model.generate_guess')
@patch('model.garbage_model.retrieve_bin_for_object')
def test_classify_object_neo4j_returns_empty_string(mock_retrieve, mock_generate):
    """Test classify_object falls back to LLM when Neo4j returns empty string."""
    from model.garbage_model import classify_object
    
    # Mock Neo4j returning empty string (falsy value)
    mock_retrieve.return_value = ""
    mock_generate.return_value = "mixed-paper"
    
    result = classify_object("newspaper")
    
    assert result == {"object_name": "newspaper", "bin_type": "mixed-paper"}
    mock_retrieve.assert_called_once_with("newspaper")
    mock_generate.assert_called_once_with("newspaper")


@pytest.mark.unit
@patch('model.garbage_model.generate_guess')
@patch('model.garbage_model.retrieve_bin_for_object')
def test_classify_object_various_bin_types(mock_retrieve, mock_generate):
    """Test classify_object with various bin types from Neo4j."""
    from model.garbage_model import classify_object
    
    test_cases = [
        ("plastic bottle", "recyclable"),
        ("banana peel", "compostable"),
        ("styrofoam", "garbage"),
        ("newspaper", "mixed-paper"),
        ("glass jar", "recyclable"),
    ]
    
    for object_name, bin_type in test_cases:
        mock_retrieve.return_value = bin_type
        mock_generate.reset_mock()
        
        result = classify_object(object_name)
        
        assert result["object_name"] == object_name
        assert result["bin_type"] == bin_type
        mock_generate.assert_not_called()


@pytest.mark.unit
@patch('model.garbage_model.generate_guess')
@patch('model.garbage_model.retrieve_bin_for_object')
def test_classify_object_llm_fallback_various_items(mock_retrieve, mock_generate):
    """Test classify_object LLM fallback with various items."""
    from model.garbage_model import classify_object
    
    test_cases = [
        ("unknown item 1", "recyclable"),
        ("mystery object", "garbage"),
        ("new product", "compostable"),
    ]
    
    for object_name, expected_bin in test_cases:
        mock_retrieve.return_value = None
        mock_generate.return_value = expected_bin
        
        result = classify_object(object_name)
        
        assert result["object_name"] == object_name
        assert result["bin_type"] == expected_bin
        mock_generate.assert_called_with(object_name)


@pytest.mark.unit
@patch('model.garbage_model.generate_guess')
@patch('model.garbage_model.retrieve_bin_for_object')
def test_classify_object_special_characters(mock_retrieve, mock_generate):
    """Test classify_object with special characters in object name."""
    from model.garbage_model import classify_object
    
    special_names = [
        "plastic bottle (16 oz.)",
        "coffee cup #1",
        "item-with-dashes",
        "item_with_underscores",
    ]
    
    for name in special_names:
        mock_retrieve.return_value = "recyclable"
        
        result = classify_object(name)
        
        assert result["object_name"] == name
        assert result["bin_type"] == "recyclable"


@pytest.mark.unit
@patch('model.garbage_model.generate_guess')
@patch('model.garbage_model.retrieve_bin_for_object')
def test_classify_object_case_sensitive(mock_retrieve, mock_generate):
    """Test that classify_object handles case-sensitive names."""
    from model.garbage_model import classify_object
    
    cases = ["Plastic Bottle", "PLASTIC BOTTLE", "plastic bottle"]
    
    for name in cases:
        mock_retrieve.return_value = "recyclable"
        
        result = classify_object(name)
        
        assert result["object_name"] == name
        mock_retrieve.assert_called_with(name)


@pytest.mark.unit
@patch('model.garbage_model.generate_guess')
@patch('model.garbage_model.retrieve_bin_for_object')
def test_classify_object_whitespace(mock_retrieve, mock_generate):
    """Test classify_object with leading/trailing whitespace."""
    from model.garbage_model import classify_object
    
    mock_retrieve.return_value = "recyclable"
    
    result = classify_object("  plastic bottle  ")
    
    assert result["object_name"] == "  plastic bottle  "
    mock_retrieve.assert_called_once_with("  plastic bottle  ")


@pytest.mark.unit
@patch('model.garbage_model.generate_guess')
@patch('model.garbage_model.retrieve_bin_for_object')
def test_classify_object_unicode_characters(mock_retrieve, mock_generate):
    """Test classify_object with unicode characters."""
    from model.garbage_model import classify_object
    
    mock_retrieve.return_value = "compostable"
    
    result = classify_object("café napkin")
    
    assert result["object_name"] == "café napkin"
    assert result["bin_type"] == "compostable"


@pytest.mark.unit
@patch('model.garbage_model.generate_guess')
@patch('model.garbage_model.retrieve_bin_for_object')
def test_classify_object_long_name(mock_retrieve, mock_generate):
    """Test classify_object with very long object name."""
    from model.garbage_model import classify_object
    
    long_name = "very long object name " * 50
    mock_retrieve.return_value = "garbage"
    
    result = classify_object(long_name)
    
    assert result["object_name"] == long_name
    assert result["bin_type"] == "garbage"


@pytest.mark.unit
@patch('model.garbage_model.generate_guess')
@patch('model.garbage_model.retrieve_bin_for_object')
def test_classify_object_return_type(mock_retrieve, mock_generate):
    """Test that classify_object always returns correct dictionary structure."""
    from model.garbage_model import classify_object
    
    mock_retrieve.return_value = "recyclable"
    
    result = classify_object("test item")
    
    # Check return type and structure
    assert isinstance(result, dict)
    assert "object_name" in result
    assert "bin_type" in result
    assert len(result) == 2


@pytest.mark.unit
@patch('model.garbage_model.generate_guess')
@patch('model.garbage_model.retrieve_bin_for_object')
def test_classify_object_both_branches_covered(mock_retrieve, mock_generate):
    """Test that both Neo4j hit and miss branches are covered."""
    from model.garbage_model import classify_object
    
    # Test Neo4j hit branch
    mock_retrieve.return_value = "recyclable"
    result1 = classify_object("item1")
    assert result1["bin_type"] == "recyclable"
    
    # Test Neo4j miss branch (None)
    mock_retrieve.return_value = None
    mock_generate.return_value = "garbage"
    result2 = classify_object("item2")
    assert result2["bin_type"] == "garbage"
    
    # Test Neo4j miss branch ("None" string)
    mock_retrieve.return_value = "None"
    mock_generate.return_value = "compostable"
    result3 = classify_object("item3")
    assert result3["bin_type"] == "compostable"


@pytest.mark.unit
@patch('model.garbage_model.generate_guess')
@patch('model.garbage_model.retrieve_bin_for_object')
def test_classify_object_empty_string_name(mock_retrieve, mock_generate):
    """Test classify_object with empty string as name."""
    from model.garbage_model import classify_object
    
    mock_retrieve.return_value = "garbage"
    
    result = classify_object("")
    
    assert result["object_name"] == ""
    assert result["bin_type"] == "garbage"
