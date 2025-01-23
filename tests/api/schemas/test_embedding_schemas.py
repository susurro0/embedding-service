import pytest
from pydantic import ValidationError

from api.schemas.embedding_schemas import EmbeddingIdRequest, EmbeddingRequest, TextRequest


# Test EmbeddingIdRequest
def test_embedding_id_request_valid():
    data = {"id": 123}
    request = EmbeddingIdRequest(**data)
    assert request.id == 123

def test_embedding_id_request_invalid():
    data = {"id": "invalid"}  # id should be an integer
    with pytest.raises(ValidationError):
        EmbeddingIdRequest(**data)

# Test EmbeddingRequest
def test_embedding_request_valid():
    data = {
        "text": "This is a test",
        "embedding": [0.1, 0.2, 0.3]
    }
    request = EmbeddingRequest(**data)
    assert request.text == "This is a test"
    assert request.embedding == [0.1, 0.2, 0.3]

def test_embedding_request_invalid_text():
    data = {
        "text": 1,  # text cannot be numbers
        "embedding": [0.1, 0.2, 0.3]
    }
    with pytest.raises(ValidationError):
        EmbeddingRequest(**data)

def test_embedding_request_invalid_embedding():
    data = {
        "text": "Valid text",
        "embedding": "invalid"  # embedding should be a list of numbers
    }
    with pytest.raises(ValidationError):
        EmbeddingRequest(**data)

# Test TextRequest
def test_text_request_valid():
    data = {
        "chunks": ["chunk 1", "chunk 2"]
    }
    request = TextRequest(**data)
    assert request.chunks == ["chunk 1", "chunk 2"]

def test_text_request_invalid_chunks():
    data = {
        "chunks": "invalid"  # chunks should be a list of strings
    }
    with pytest.raises(ValidationError):
        TextRequest(**data)
