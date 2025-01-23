import pytest
from peewee import SqliteDatabase

from app.models.models import Embedding


# Use an in-memory SQLite database for testing
@pytest.fixture
def test_db():
    db = SqliteDatabase(':memory:')
    db.bind([Embedding], bind_refs=False, bind_backrefs=False)
    db.connect()
    db.create_tables([Embedding])
    yield db
    db.drop_tables([Embedding])
    db.close()

def test_create_embedding(test_db):
    # Test creation of an embedding record
    embedding = Embedding.create(
        text="Test text",
        embedding='[1.0, 2.0, 3.0]'
    )
    assert embedding.id is not None
    assert embedding.text == "Test text"
    assert embedding.embedding == '[1.0, 2.0, 3.0]'

def test_query_embedding(test_db):
    # Insert a record and query it
    embedding = Embedding.create(
        text="Query test",
        embedding='[4.0, 5.0, 6.0]'
    )
    queried_embedding = Embedding.get_by_id(embedding.id)
    assert queried_embedding.text == "Query test"
    assert queried_embedding.embedding == '[4.0, 5.0, 6.0]'

def test_update_embedding(test_db):
    # Test updating an existing record
    embedding = Embedding.create(
        text="Update test",
        embedding='[7.0, 8.0, 9.0]'
    )
    embedding.text = "Updated text"
    embedding.save()

    updated_embedding = Embedding.get_by_id(embedding.id)
    assert updated_embedding.text == "Updated text"

def test_delete_embedding(test_db):
    # Test deleting a record
    embedding = Embedding.create(
        text="Delete test",
        embedding='[10.0, 11.0, 12.0]'
    )
    embedding_id = embedding
