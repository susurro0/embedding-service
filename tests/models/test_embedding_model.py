import json
from unittest.mock import patch

import numpy as np
import pytest
from peewee import SqliteDatabase
from torch.nn.functional import embedding

from app.models.embedding_model import Embedding


# Use an in-memory SQLite database for testing
@pytest.fixture
def mock_database():
    db = SqliteDatabase(':memory:')  # Use an in-memory SQLite database
    db.connect()
    db.create_tables([Embedding])  # Create the tables for the model
    yield db  # Provide the database for the tests
    db.drop_tables([Embedding])  # Drop the tables after tests are done
    db.close()

def test_create_embedding(mock_database):
    # Test creation of an embedding record
    with patch("app.models.embedding_model.database_instance", return_value=mock_database):
        embedding_data = [1.0] * 384
        embedding = Embedding.create(
            text="Test text",
            embedding = embedding_data
        )
        assert embedding.id is not None
        assert embedding.text == "Test text"
        assert embedding.embedding == embedding_data


def test_query_embedding(mock_database):
    # Insert a record and query it
    with patch("app.models.embedding_model.database_instance", return_value=mock_database):
        created_embedding = Embedding.create(
            text="Query test",
            embedding=[1.0] * 384
        )
        queried_embedding = Embedding.get_by_id(created_embedding.id)
        assert queried_embedding.text == "Query test"
        assert (queried_embedding.embedding == [1.0] * 384).all()

def test_update_embedding(mock_database):
    # Test updating an existing record
    with patch("app.models.embedding_model.database_instance", return_value=mock_database):

        embedding = Embedding.create(
                text="Update test",
                embedding=[1.0] * 384
            )
        embedding.text = "Updated text"
        embedding.save()

    updated_embedding = Embedding.get_by_id(embedding.id)
    assert updated_embedding.text == "Updated text"

def test_delete_embedding(mock_database):
    # Test deleting a record
    with patch("app.models.embedding_model.database_instance", return_value=mock_database):

        embedding = Embedding.create(
            text="Delete test",
            embedding=[1.0] * 384
        )
        embedding_id = embedding
        embedding.delete_instance()
        with pytest.raises(Embedding.DoesNotExist):
            Embedding.get_by_id(embedding_id)