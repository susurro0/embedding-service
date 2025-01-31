import json
import pytest
from unittest.mock import patch, MagicMock, call

from fastapi import HTTPException
from peewee import SqliteDatabase

from crud.embedding_crud import EmbeddingCRUD
from database.database import database_instance
from models.embedding_model import Embedding



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

    embeddings = [
        [0.1] * 384,  # Padded to 384
        [0.3] * 384  # Padded to 384
    ]

    # Patch database_instance to use the mock database
    with patch("app.models.embedding_model.database_instance", return_value=mock_database):
        # Mock the Embedding.create method to avoid real database interaction
        with patch("app.models.embedding_model.Embedding.create") as spy_create:
            # Simulate the behavior of the create method with different returns for each call
            spy_create.side_effect = [
                MagicMock(id=1, text="chunk1", embedding=[0.1] * 384),
                MagicMock(id=2, text="chunk2", embedding=[0.3] * 384)
            ]

            # Create a CRUD instance and run the save_embedding method
            crud = EmbeddingCRUD()
            result = crud.save_embedding(chunks, embeddings)

            # Ensure the `create` method was called the correct number of times
            assert spy_create.call_count == 2

            # Verify the arguments passed to `create` using unittest.mock.call
            spy_create.assert_has_calls([
                call(text="chunk1", embedding=[0.1] * 384),
                call(text="chunk2", embedding=[0.3] * 384)
            ])

            # Verify the returned result (mocked instances)
            assert len(result) == 2
            assert result[0].text == "chunk1"
            assert result[1].text == "chunk2"

            # Ensure the mocked result has the correct ids
            assert result[0].id == 1
            assert result[1].id == 2


def test_get_embedding_by_id_valid(mock_database):
    # Create a sample embedding in the database
    with patch("app.models.embedding_model.database_instance", return_value=mock_database):
        valid_embedding = [0.1] * 384

        # Store the embedding directly (no JSON serialization)
        embedding_instance = Embedding.create(
            text="Test chunk",
            embedding=valid_embedding  # Store as a list of floats
        )

        crud = EmbeddingCRUD()
        result = crud.get_embedding_by_id(embedding_instance.id)

        # Verify the result
        assert result is not None
        embedding_instance_result, embedding_data = result

        # The 'embedding' field should be returned as the list of floats
        assert embedding_instance_result.id == embedding_instance.id
        assert len(embedding_data) == len(valid_embedding)


def test_get_embedding_by_id_invalid_json(mock_database):
    # Create a sample embedding with invalid JSON
    with patch("app.models.embedding_model.database_instance", return_value=mock_database):
        with patch("app.models.embedding_model.Embedding.get_or_none", return_value=Exception('Throw an exception')):

            crud = EmbeddingCRUD()
            # result = crud.get_embedding_by_id(embedding_instance.id)
            with pytest.raises(HTTPException, match="404: Embedding not found"):
                result = crud.get_embedding_by_id(1)
                # Verify the result is None due to invalid JSON
                assert result is None


def test_get_embedding_by_id_not_found(mock_database):
    crud = EmbeddingCRUD()
    result = crud.get_embedding_by_id(999)  # Non-existent ID

    # Verify the result is None
    assert result is None
