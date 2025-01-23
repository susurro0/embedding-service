import pytest
from unittest.mock import patch, MagicMock
import json

from app.utils.embedding_utils import compute_embedding_from_text, compute_embeddings_from_texts, \
    convert_embedding_to_float_list


@pytest.fixture
def mock_model():
    """Mock the SentenceTransformer model."""
    mock = MagicMock()
    mock.encode.side_effect = lambda x: [[1.0, 2.0, 3.0]] if isinstance(x, str) else [[1.0, 2.0, 3.0] for _ in x]
    return mock


@patch("app.utils.embedding_utils.model", new_callable=lambda: MagicMock())
def test_compute_embedding_from_text(mock_model):
    """Test compute_embedding_from_text."""
    # Arrange
    mock_model.encode.return_value = [1.0, 2.0, 3.0]
    text = "Test input text"

    # Act
    embedding = compute_embedding_from_text(text)

    # Assert
    mock_model.encode.assert_called_once_with(text)
    assert embedding == [1.0, 2.0, 3.0]


@patch("app.utils.embedding_utils.model", new_callable=lambda: MagicMock())
def test_compute_embeddings_from_texts(mock_model):
    """Test compute_embeddings_from_texts."""
    # Arrange
    texts = ["Test input 1", "Test input 2"]
    mock_model.encode.return_value = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]

    # Act
    embeddings = compute_embeddings_from_texts(texts)

    # Assert
    mock_model.encode.assert_called_once_with(texts)
    assert embeddings == [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]


def test_convert_embedding_to_float_list_valid_string():
    """Test convert_embedding_to_float_list with a valid string embedding."""
    # Arrange
    class MockEmbeddingInstance:
        embedding = "1.0 2.0 3.0"

    embedding_instance = MockEmbeddingInstance()

    # Act
    result = convert_embedding_to_float_list(embedding_instance)

    # Assert
    assert result == [1.0, 2.0, 3.0]


def test_convert_embedding_to_float_list_json_string():
    """Test convert_embedding_to_float_list with a JSON string embedding."""
    # Arrange
    class MockEmbeddingInstance:
        embedding = json.dumps([1.0, 2.0, 3.0])

    embedding_instance = MockEmbeddingInstance()

    # Act
    result = convert_embedding_to_float_list(embedding_instance)

    # Assert
    assert result == [1.0, 2.0, 3.0]


def test_convert_embedding_to_float_list_invalid_format():
    """Test convert_embedding_to_float_list with an invalid format."""
    # Arrange
    class MockEmbeddingInstance:
        embedding = "invalid string"

    embedding_instance = MockEmbeddingInstance()

    # Act & Assert
    with pytest.raises(ValueError, match="Failed to parse embedding"):
        convert_embedding_to_float_list(embedding_instance)


def test_convert_embedding_to_float_list_missing_attribute():
    """Test convert_embedding_to_float_list with missing embedding attribute."""
    # Arrange
    class MockEmbeddingInstance:
        pass

    embedding_instance = MockEmbeddingInstance()

    # Act & Assert
    with pytest.raises(ValueError, match="Failed to parse embedding"):
        convert_embedding_to_float_list(embedding_instance)
