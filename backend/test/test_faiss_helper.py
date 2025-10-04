"""
Comprehensive unit tests for faiss_helper.py to achieve 100% code coverage.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch, call
import numpy as np
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.unit
@patch('faiss_helper.driver')
def test_get_all_embeddings(mock_driver, sample_embeddings, sample_item_names):
    """Test getting all embeddings from Neo4j."""
    from faiss_helper import get_all_embeddings
    
    # Mock Neo4j session and results
    mock_session = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    
    # Create mock records
    mock_records = []
    for name, embedding in zip(sample_item_names[:3], sample_embeddings[:3]):
        mock_record = MagicMock()
        mock_record.__getitem__ = lambda self, key, n=name, e=embedding.tolist(): n if key == 'name' else e
        mock_records.append(mock_record)
    
    mock_session.run.return_value = mock_records
    
    item_names, embeddings = get_all_embeddings()
    
    assert len(item_names) == 3
    assert embeddings.shape[0] == 3
    assert embeddings.dtype == np.float32


@pytest.mark.unit
def test_build_faiss_index(sample_embeddings):
    """Test building FAISS index from embeddings."""
    from faiss_helper import build_faiss_index
    
    index = build_faiss_index(sample_embeddings)
    
    assert index.ntotal == len(sample_embeddings)
    assert index.d == sample_embeddings.shape[1]


@pytest.mark.unit
@patch('faiss_helper.faiss.write_index')
def test_save_faiss_index(mock_write_index, mock_faiss_index):
    """Test saving FAISS index to file."""
    from faiss_helper import save_faiss_index
    
    save_faiss_index(mock_faiss_index, 'test.index')
    
    mock_write_index.assert_called_once_with(mock_faiss_index, 'test.index')


@pytest.mark.unit
@patch('faiss_helper.faiss.write_index')
def test_save_faiss_index_default_path(mock_write_index, mock_faiss_index):
    """Test saving FAISS index with default file path."""
    from faiss_helper import save_faiss_index
    
    save_faiss_index(mock_faiss_index)
    
    mock_write_index.assert_called_once_with(mock_faiss_index, 'faiss.index')


@pytest.mark.unit
@patch('faiss_helper.np.save')
@patch('faiss_helper.faiss.read_index')
@patch('faiss_helper.os.path.exists')
def test_load_faiss_index_file_exists(mock_exists, mock_read_index, mock_np_save, mock_faiss_index):
    """Test loading FAISS index when file exists."""
    from faiss_helper import load_faiss_index
    
    mock_exists.return_value = True
    mock_read_index.return_value = mock_faiss_index
    
    index = load_faiss_index('existing.index')
    
    assert index == mock_faiss_index
    mock_read_index.assert_called_once_with('existing.index')
    mock_np_save.assert_not_called()


@pytest.mark.unit
@patch('faiss_helper.save_faiss_index')
@patch('faiss_helper.build_faiss_index')
@patch('faiss_helper.get_all_embeddings')
@patch('faiss_helper.np.save')
@patch('faiss_helper.os.path.exists')
def test_load_faiss_index_file_not_exists(mock_exists, mock_np_save, mock_get_embeddings, 
                                          mock_build_index, mock_save_index,
                                          sample_embeddings, sample_item_names, mock_faiss_index):
    """Test loading FAISS index when file doesn't exist - builds new index."""
    from faiss_helper import load_faiss_index
    
    mock_exists.return_value = False
    mock_get_embeddings.return_value = (sample_item_names[:5], sample_embeddings[:5])
    mock_build_index.return_value = mock_faiss_index
    
    index = load_faiss_index('nonexistent.index')
    
    assert index == mock_faiss_index
    mock_get_embeddings.assert_called_once()
    mock_build_index.assert_called_once()
    mock_save_index.assert_called_once_with(mock_faiss_index, 'nonexistent.index')
    mock_np_save.assert_called_once()


@pytest.mark.unit
@patch('faiss_helper.save_faiss_index')
@patch('faiss_helper.build_faiss_index')
@patch('faiss_helper.get_all_embeddings')
@patch('faiss_helper.np.save')
def test_update_faiss_index(mock_np_save, mock_get_embeddings, mock_build_index, 
                           mock_save_index, sample_embeddings, sample_item_names, mock_faiss_index):
    """Test updating FAISS index."""
    from faiss_helper import update_faiss_index
    
    mock_get_embeddings.return_value = (sample_item_names, sample_embeddings)
    mock_build_index.return_value = mock_faiss_index
    
    index, item_names = update_faiss_index()
    
    assert index == mock_faiss_index
    assert item_names == sample_item_names
    mock_get_embeddings.assert_called_once()
    mock_build_index.assert_called_once()
    mock_save_index.assert_called_once()
    mock_np_save.assert_called_once()


@pytest.mark.unit
def test_search_similar_items(mock_faiss_index, sample_item_names):
    """Test searching for similar items."""
    from faiss_helper import search_similar_items
    
    query_embedding = [0.1] * 1536
    
    similar_items = search_similar_items(query_embedding, mock_faiss_index, sample_item_names, top_k=5)
    
    assert len(similar_items) == 5
    assert all(item in sample_item_names for item in similar_items)
    mock_faiss_index.search.assert_called_once()


@pytest.mark.unit
def test_search_similar_items_top_k_varies(mock_faiss_index, sample_item_names):
    """Test searching with different top_k values."""
    from faiss_helper import search_similar_items
    
    query_embedding = [0.1] * 1536
    
    for k in [1, 3, 5, 10]:
        mock_faiss_index.search.return_value = (
            np.array([[0.1] * k]),
            np.array([list(range(k))])
        )
        
        similar_items = search_similar_items(query_embedding, mock_faiss_index, 
                                            sample_item_names, top_k=k)
        
        assert len(similar_items) == k


@pytest.mark.unit
def test_search_similar_items_embedding_reshape(mock_faiss_index, sample_item_names):
    """Test that query embedding is properly reshaped."""
    from faiss_helper import search_similar_items
    
    # Test with 1D array
    query_embedding = [0.1] * 1536
    
    search_similar_items(query_embedding, mock_faiss_index, sample_item_names)
    
    # Verify search was called and embedding was reshaped to 2D
    call_args = mock_faiss_index.search.call_args
    query_array = call_args[0][0]
    assert query_array.shape == (1, 1536)
    assert query_array.dtype == np.float32


@pytest.mark.unit
@patch('faiss_helper.driver')
def test_get_all_embeddings_empty_result(mock_driver):
    """Test get_all_embeddings with no data."""
    from faiss_helper import get_all_embeddings
    
    mock_session = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    mock_session.run.return_value = []
    
    item_names, embeddings = get_all_embeddings()
    
    assert len(item_names) == 0
    assert embeddings.shape[0] == 0


@pytest.mark.unit
def test_build_faiss_index_single_embedding():
    """Test building FAISS index with single embedding."""
    from faiss_helper import build_faiss_index
    
    single_embedding = np.random.rand(1, 1536).astype('float32')
    
    index = build_faiss_index(single_embedding)
    
    assert index.ntotal == 1
    assert index.d == 1536


@pytest.mark.unit
def test_build_faiss_index_large_dataset():
    """Test building FAISS index with large dataset."""
    from faiss_helper import build_faiss_index
    
    large_embeddings = np.random.rand(1000, 1536).astype('float32')
    
    index = build_faiss_index(large_embeddings)
    
    assert index.ntotal == 1000


@pytest.mark.unit
@patch('faiss_helper.driver')
def test_get_all_embeddings_query_format(mock_driver):
    """Test that get_all_embeddings uses correct Cypher query."""
    from faiss_helper import get_all_embeddings
    
    mock_session = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    mock_session.run.return_value = []
    
    get_all_embeddings()
    
    # Verify the Cypher query was called
    call_args = mock_session.run.call_args
    query = call_args[0][0]
    assert "MATCH (i:Item)" in query
    assert "i.name" in query
    assert "i.embedding" in query


@pytest.mark.unit
def test_search_similar_items_returns_correct_items(sample_item_names):
    """Test that search returns items in correct order based on indices."""
    from faiss_helper import search_similar_items
    
    # Create a mock index that returns specific indices
    mock_index = MagicMock()
    mock_index.search.return_value = (
        np.array([[0.1, 0.2, 0.3]]),
        np.array([[2, 0, 4]])  # Specific indices
    )
    
    query_embedding = [0.1] * 1536
    
    similar_items = search_similar_items(query_embedding, mock_index, sample_item_names, top_k=3)
    
    # Should return items at indices 2, 0, 4 in that order
    expected_items = [sample_item_names[2], sample_item_names[0], sample_item_names[4]]
    assert similar_items == expected_items


@pytest.mark.unit
@patch('faiss_helper.np.save')
@patch('faiss_helper.save_faiss_index')
@patch('faiss_helper.build_faiss_index')
@patch('faiss_helper.get_all_embeddings')
def test_update_faiss_index_saves_item_names(mock_get_embeddings, mock_build_index,
                                             mock_save_index, mock_np_save,
                                             sample_embeddings, sample_item_names, mock_faiss_index):
    """Test that update_faiss_index saves item names."""
    from faiss_helper import update_faiss_index
    
    mock_get_embeddings.return_value = (sample_item_names, sample_embeddings)
    mock_build_index.return_value = mock_faiss_index
    
    update_faiss_index()
    
    # Verify item names are saved
    mock_np_save.assert_called_once()
    call_args = mock_np_save.call_args
    assert call_args[0][0] == 'item_names.npy'
    np.testing.assert_array_equal(call_args[0][1], np.array(sample_item_names))


@pytest.mark.unit
@patch('faiss_helper.np.save')
@patch('faiss_helper.save_faiss_index')
@patch('faiss_helper.build_faiss_index')
@patch('faiss_helper.get_all_embeddings')
@patch('faiss_helper.os.path.exists')
def test_load_faiss_index_default_path(mock_exists, mock_get_embeddings, mock_build_index,
                                       mock_save_index, mock_np_save,
                                       sample_embeddings, sample_item_names, mock_faiss_index):
    """Test load_faiss_index with default file path."""
    from faiss_helper import load_faiss_index
    
    mock_exists.return_value = False
    mock_get_embeddings.return_value = (sample_item_names, sample_embeddings)
    mock_build_index.return_value = mock_faiss_index
    
    index = load_faiss_index()
    
    # Should use default 'faiss.index' path
    mock_exists.assert_called_once_with('faiss.index')
    mock_save_index.assert_called_once_with(mock_faiss_index, 'faiss.index')


@pytest.mark.unit
def test_search_similar_items_default_top_k(sample_item_names):
    """Test search_similar_items with default top_k=10."""
    from faiss_helper import search_similar_items
    
    mock_index = MagicMock()
    mock_index.search.return_value = (
        np.array([[0.1] * 10]),
        np.array([list(range(10))])
    )
    
    query_embedding = [0.1] * 1536
    
    similar_items = search_similar_items(query_embedding, mock_index, sample_item_names)
    
    # Default top_k should be 10
    assert len(similar_items) == 10


@pytest.mark.unit
@patch('faiss_helper.driver')
def test_get_all_embeddings_converts_to_numpy(mock_driver):
    """Test that get_all_embeddings converts embeddings to numpy array."""
    from faiss_helper import get_all_embeddings
    
    mock_session = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    
    # Create mock records with list embeddings
    mock_record = MagicMock()
    mock_record.__getitem__ = lambda self, key: 'item1' if key == 'name' else [0.1] * 1536
    mock_session.run.return_value = [mock_record]
    
    item_names, embeddings = get_all_embeddings()
    
    assert isinstance(embeddings, np.ndarray)
    assert embeddings.dtype == np.float32
