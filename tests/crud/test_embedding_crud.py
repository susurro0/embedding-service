import json
import pytest
from unittest.mock import patch, MagicMock, call

from peewee import SqliteDatabase

from crud.embedding_crud import EmbeddingCRUD
from models.models import Embedding


@pytest.fixture
def mock_database():
    db = SqliteDatabase(":memory:")
    db.connect()
    db.create_tables([Embedding])
    yield db
    db.drop_tables([Embedding])
    db.close()

def test_save_embedding_spy(mock_database):
    chunks = ["chunk1", "chunk2"]
    embeddings = [[0.1, 0.2], [0.3, 0.4]]

    # Spy on the Embedding model's `create` method
    with patch("app.models.models.Embedding.create", wraps=Embedding.create) as spy_create:
        crud = EmbeddingCRUD()
        result = crud.save_embedding(chunks, embeddings)

        # Ensure the `create` method was called the correct number of times
        assert spy_create.call_count == 2

        # Verify the arguments passed to `create`
        spy_create.assert_has_calls([
            call(text="chunk1", embedding=str([0.1, 0.2])),
            call(text="chunk2", embedding=str([0.3, 0.4]))
        ])

        # Verify the returned result
        assert len(result) == 2
        assert result[0].text == "chunk1"
        assert result[1].text == "chunk2"

def test_get_embedding_by_id_valid(mock_database):
    # Create a sample embedding in the database
    valid_embedding = {"key": "value", "numbers": [1.0, 2.0, 3.0]}
    embedding_instance = Embedding.create(
        text="Test chunk",
        embedding=json.dumps(valid_embedding)  # Store as a JSON string
    )

    crud = EmbeddingCRUD()
    result = crud.get_embedding_by_id(embedding_instance.id)

    # Verify the result
    assert result is not None
    embedding_instance_result, embedding_data = result

    assert embedding_instance_result.id == embedding_instance.id
    assert embedding_data == valid_embedding


def test_get_embedding_by_id_invalid_json(mock_database):
    # Create a sample embedding with invalid JSON
    invalid_embedding = "invalid json string"
    embedding_instance = Embedding.create(
        text="Test chunk",
        embedding=invalid_embedding
    )

    crud = EmbeddingCRUD()
    result = crud.get_embedding_by_id(embedding_instance.id)

    # Verify the result is None due to invalid JSON
    assert result is None


def test_get_embedding_by_id_not_found(mock_database):
    crud = EmbeddingCRUD()
    result = crud.get_embedding_by_id(999)  # Non-existent ID

    # Verify the result is None
    assert result is None
