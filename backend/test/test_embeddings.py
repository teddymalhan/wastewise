"""
Comprehensive unit tests for embeddings.py to achieve 100% code coverage.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open, call
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.unit
@patch('embeddings.openai.embeddings.create')
def test_generate_embedding_success(mock_create):
    """Test successful embedding generation."""
    from embeddings import generate_embedding
    
    # Mock OpenAI response
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=[0.1] * 1536)]
    mock_create.return_value = mock_response
    
    embedding = generate_embedding("plastic bottle")
    
    assert len(embedding) == 1536
    assert all(isinstance(x, float) for x in embedding)
    mock_create.assert_called_once()


@pytest.mark.unit
@patch('embeddings.openai.embeddings.create')
def test_generate_embedding_correct_model(mock_create):
    """Test that correct model is used for embedding generation."""
    from embeddings import generate_embedding
    
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=[0.1] * 1536)]
    mock_create.return_value = mock_response
    
    generate_embedding("test item")
    
    call_args = mock_create.call_args
    assert call_args[1]['model'] == "text-embedding-ada-002"
    assert call_args[1]['input'] == "test item"


@pytest.mark.unit
@patch('embeddings.openai.embeddings.create')
def test_generate_embedding_various_items(mock_create):
    """Test embedding generation with various item names."""
    from embeddings import generate_embedding
    
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=[0.1] * 1536)]
    mock_create.return_value = mock_response
    
    test_items = [
        "plastic bottle",
        "banana peel",
        "glass jar",
        "cardboard box",
        "aluminum can"
    ]
    
    for item in test_items:
        embedding = generate_embedding(item)
        assert len(embedding) == 1536


@pytest.mark.unit
@patch('embeddings.driver')
def test_store_in_neo4j_success(mock_driver):
    """Test successful storage in Neo4j."""
    from embeddings import store_in_neo4j
    
    mock_session = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    
    embedding = [0.1] * 1536
    store_in_neo4j("plastic bottle", "recyclable", embedding)
    
    # Verify session.run was called
    mock_session.run.assert_called_once()


@pytest.mark.unit
@patch('embeddings.driver')
def test_store_in_neo4j_query_structure(mock_driver):
    """Test that correct Cypher query is used in store_in_neo4j."""
    from embeddings import store_in_neo4j
    
    mock_session = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    
    embedding = [0.1] * 1536
    store_in_neo4j("test item", "garbage", embedding)
    
    call_args = mock_session.run.call_args
    query = call_args[0][0]
    
    assert "CREATE (i:Item {name: $item_name, embedding: $embedding})" in query
    assert "CREATE (b:Bin {type: $bin_type})" in query
    assert "CREATE (i)-[:SHOULD_GO_IN]->(b)" in query


@pytest.mark.unit
@patch('embeddings.driver')
def test_store_in_neo4j_parameters(mock_driver):
    """Test that correct parameters are passed to Neo4j."""
    from embeddings import store_in_neo4j
    
    mock_session = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    
    embedding = [0.5] * 1536
    store_in_neo4j("glass jar", "recyclable", embedding)
    
    call_args = mock_session.run.call_args
    params = call_args[1]
    
    assert params['item_name'] == "glass jar"
    assert params['bin_type'] == "recyclable"
    assert params['embedding'] == embedding


@pytest.mark.unit
@patch('embeddings.driver')
def test_store_in_neo4j_various_bin_types(mock_driver):
    """Test storing items with various bin types."""
    from embeddings import store_in_neo4j
    
    mock_session = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    
    bin_types = ["recyclable", "compostable", "garbage", "mixed-paper"]
    embedding = [0.1] * 1536
    
    for bin_type in bin_types:
        store_in_neo4j(f"item_{bin_type}", bin_type, embedding)
        
        call_args = mock_session.run.call_args
        params = call_args[1]
        assert params['bin_type'] == bin_type


@pytest.mark.unit
@patch('embeddings.generate_embedding')
@patch('embeddings.store_in_neo4j')
@patch('builtins.open', new_callable=mock_open, read_data='item_name,bin_type\nplastic bottle,recyclable\nbanana peel,compostable\n')
@patch('embeddings.csv.DictReader')
def test_process_csv_and_store_success(mock_csv_reader, mock_file, mock_store, mock_generate):
    """Test processing CSV and storing data."""
    from embeddings import process_csv_and_store
    
    # Mock CSV rows
    mock_csv_reader.return_value = [
        {'item_name': 'plastic bottle', 'bin_type': 'recyclable'},
        {'item_name': 'banana peel', 'bin_type': 'compostable'},
    ]
    
    # Mock embedding generation
    mock_generate.return_value = [0.1] * 1536
    
    process_csv_and_store("test.csv")
    
    # Verify embeddings were generated
    assert mock_generate.call_count == 2
    
    # Verify data was stored
    assert mock_store.call_count == 2


@pytest.mark.unit
@patch('embeddings.generate_embedding')
@patch('embeddings.store_in_neo4j')
@patch('builtins.open', new_callable=mock_open)
@patch('embeddings.csv.DictReader')
def test_process_csv_and_store_correct_calls(mock_csv_reader, mock_file, mock_store, mock_generate):
    """Test that process_csv_and_store makes correct function calls."""
    from embeddings import process_csv_and_store
    
    mock_csv_reader.return_value = [
        {'item_name': 'glass jar', 'bin_type': 'recyclable'},
    ]
    
    embedding = [0.2] * 1536
    mock_generate.return_value = embedding
    
    process_csv_and_store("test.csv")
    
    mock_generate.assert_called_once_with('glass jar')
    mock_store.assert_called_once_with('glass jar', 'recyclable', embedding)


@pytest.mark.unit
@patch('embeddings.generate_embedding')
@patch('embeddings.store_in_neo4j')
@patch('builtins.open', new_callable=mock_open)
@patch('embeddings.csv.DictReader')
def test_process_csv_and_store_handles_empty_csv(mock_csv_reader, mock_file, mock_store, mock_generate):
    """Test processing empty CSV file."""
    from embeddings import process_csv_and_store
    
    mock_csv_reader.return_value = []
    
    process_csv_and_store("empty.csv")
    
    # No embeddings should be generated or stored
    mock_generate.assert_not_called()
    mock_store.assert_not_called()


@pytest.mark.unit
@patch('embeddings.generate_embedding')
@patch('embeddings.store_in_neo4j')
@patch('builtins.open', new_callable=mock_open)
@patch('embeddings.csv.DictReader')
def test_process_csv_and_store_multiple_items(mock_csv_reader, mock_file, mock_store, mock_generate):
    """Test processing CSV with multiple items."""
    from embeddings import process_csv_and_store
    
    test_data = [
        {'item_name': 'plastic bottle', 'bin_type': 'recyclable'},
        {'item_name': 'banana peel', 'bin_type': 'compostable'},
        {'item_name': 'styrofoam', 'bin_type': 'garbage'},
        {'item_name': 'newspaper', 'bin_type': 'mixed-paper'},
    ]
    mock_csv_reader.return_value = test_data
    mock_generate.return_value = [0.1] * 1536
    
    process_csv_and_store("multi.csv")
    
    assert mock_generate.call_count == 4
    assert mock_store.call_count == 4


@pytest.mark.unit
@patch('embeddings.generate_embedding')
@patch('embeddings.store_in_neo4j')
@patch('builtins.open', new_callable=mock_open)
@patch('embeddings.csv.DictReader')
@patch('builtins.print')
def test_process_csv_and_store_prints_success(mock_print, mock_csv_reader, mock_file, 
                                              mock_store, mock_generate):
    """Test that success messages are printed."""
    from embeddings import process_csv_and_store
    
    mock_csv_reader.return_value = [
        {'item_name': 'test item', 'bin_type': 'recyclable'},
    ]
    mock_generate.return_value = [0.1] * 1536
    
    process_csv_and_store("test.csv")
    
    # Check that success message was printed
    print_calls = [str(call) for call in mock_print.call_args_list]
    assert any("Stored item 'test item'" in str(call) for call in print_calls)


@pytest.mark.unit
@patch('embeddings.generate_embedding')
@patch('embeddings.store_in_neo4j')
@patch('builtins.open', new_callable=mock_open)
@patch('embeddings.csv.DictReader')
@patch('builtins.print')
def test_process_csv_and_store_handles_none_embedding(mock_print, mock_csv_reader, 
                                                       mock_file, mock_store, mock_generate):
    """Test handling when embedding generation returns None."""
    from embeddings import process_csv_and_store
    
    mock_csv_reader.return_value = [
        {'item_name': 'failed item', 'bin_type': 'recyclable'},
    ]
    mock_generate.return_value = None
    
    process_csv_and_store("test.csv")
    
    # store_in_neo4j should not be called
    mock_store.assert_not_called()
    
    # Error message should be printed
    print_calls = [str(call) for call in mock_print.call_args_list]
    assert any("Failed to generate embedding" in str(call) for call in print_calls)


@pytest.mark.unit
@patch('embeddings.openai.embeddings.create')
def test_generate_embedding_special_characters(mock_create):
    """Test embedding generation with special characters."""
    from embeddings import generate_embedding
    
    mock_response = MagicMock()
    mock_response.data = [MagicMock(embedding=[0.1] * 1536)]
    mock_create.return_value = mock_response
    
    special_items = [
        "plastic bottle (16 oz.)",
        "item-with-dashes",
        "item_with_underscores",
        "café napkin"
    ]
    
    for item in special_items:
        embedding = generate_embedding(item)
        assert len(embedding) == 1536


@pytest.mark.unit
@patch('embeddings.driver')
def test_store_in_neo4j_special_characters(mock_driver):
    """Test storing items with special characters."""
    from embeddings import store_in_neo4j
    
    mock_session = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    
    embedding = [0.1] * 1536
    special_name = "plastic bottle (16 oz.)"
    
    store_in_neo4j(special_name, "recyclable", embedding)
    
    call_args = mock_session.run.call_args
    params = call_args[1]
    assert params['item_name'] == special_name


@pytest.mark.unit
def test_module_imports():
    """Test that embeddings module can be imported successfully."""
    import embeddings
    
    # Check that all required functions are available
    assert hasattr(embeddings, 'generate_embedding')
    assert hasattr(embeddings, 'store_in_neo4j')
    assert hasattr(embeddings, 'process_csv_and_store')


@pytest.mark.unit
@patch('embeddings.generate_embedding')
@patch('embeddings.store_in_neo4j')
@patch('builtins.open', new_callable=mock_open)
@patch('embeddings.csv.DictReader')
def test_process_csv_and_store_preserves_order(mock_csv_reader, mock_file, 
                                               mock_store, mock_generate):
    """Test that CSV rows are processed in order."""
    from embeddings import process_csv_and_store
    
    test_data = [
        {'item_name': 'item1', 'bin_type': 'bin1'},
        {'item_name': 'item2', 'bin_type': 'bin2'},
        {'item_name': 'item3', 'bin_type': 'bin3'},
    ]
    mock_csv_reader.return_value = test_data
    mock_generate.return_value = [0.1] * 1536
    
    process_csv_and_store("test.csv")
    
    # Verify calls were made in order
    generate_calls = mock_generate.call_args_list
    assert generate_calls[0][0][0] == 'item1'
    assert generate_calls[1][0][0] == 'item2'
    assert generate_calls[2][0][0] == 'item3'


@pytest.mark.unit
@patch('embeddings.driver')
def test_store_in_neo4j_embedding_format(mock_driver):
    """Test that embedding is stored in correct format."""
    from embeddings import store_in_neo4j
    
    mock_session = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    
    embedding = list(range(1536))  # Use distinct values
    store_in_neo4j("test", "recyclable", embedding)
    
    call_args = mock_session.run.call_args
    params = call_args[1]
    stored_embedding = params['embedding']
    
    # Verify embedding is stored as is
    assert stored_embedding == embedding
    assert len(stored_embedding) == 1536


@pytest.mark.unit
@patch('embeddings.generate_embedding')
@patch('embeddings.store_in_neo4j')
@patch('builtins.open', new_callable=mock_open)
@patch('embeddings.csv.DictReader')
def test_process_csv_and_store_handles_mixed_success(mock_csv_reader, mock_file,
                                                     mock_store, mock_generate):
    """Test processing CSV where some embeddings succeed and some fail."""
    from embeddings import process_csv_and_store
    
    mock_csv_reader.return_value = [
        {'item_name': 'success1', 'bin_type': 'recyclable'},
        {'item_name': 'fail1', 'bin_type': 'garbage'},
        {'item_name': 'success2', 'bin_type': 'compostable'},
    ]
    
    # First and third calls succeed, second fails
    mock_generate.side_effect = [[0.1] * 1536, None, [0.2] * 1536]
    
    process_csv_and_store("test.csv")
    
    # Only successful embeddings should be stored
    assert mock_store.call_count == 2
    
    # Verify correct items were stored
    store_calls = mock_store.call_args_list
    assert store_calls[0][0][0] == 'success1'
    assert store_calls[1][0][0] == 'success2'
