from fastapi import FastAPI

from api.endpoints import EmbeddingRoutes
from unittest.mock import MagicMock, create_autospec, patch
from fastapi.testclient import TestClient

import pytest

from app.crud.embedding_crud import EmbeddingCRUD
from app.core.dependencies import Dependency
from app.models.embedding_model import Embedding


@pytest.fixture
def mock_embedding_crud():
    mock_crud = MagicMock(EmbeddingCRUD)
    mock_crud.save_embedding = MagicMock()
    mock_crud.get_embedding_by_id = MagicMock()
    return mock_crud

@pytest.fixture
def client(mock_embedding_crud):
    app = FastAPI()
    # Create a mock for the Dependency
    mock_dependency = MagicMock(spec=Dependency)
    mock_dependency.get_db = MagicMock()

    # Initialize the DocumentRoutes with mocked dependencies
    embedding_routes = EmbeddingRoutes(dependency=mock_dependency, embedding_crud=mock_embedding_crud)
    # Pass the mocked EmbeddingCRUD to the app
    app.include_router(embedding_routes.router)
    return TestClient(app)


# Test for the POST /embedding/text/ endpoint
def test_create_embedding_from_text(client, mock_embedding_crud):
    # Prepare mock data
    mock_chunks = ["This is the first chunk.", "Here is the second chunk."]
    mock_embeddings = [
        [0.1, 0.2, 0.3],  # Mocked embedding vectors
        [0.4, 0.5, 0.6]
    ]
    mock_embedding_instance = MagicMock()
    mock_embedding_instance.embedding = "0.1 0.2 0.3"
    mock_embedding_crud.save_embedding.return_value = [mock_embedding_instance, mock_embedding_instance]
    # Mock payload
    request_data = {"chunks": mock_chunks}

    # Make the POST request
    response = client.post("/embedding/text/", json=request_data)

    # Assertions

    assert response.status_code == 200
    response_data = response.json()
    assert "embeddings" in response_data
    assert len(response_data["embeddings"]) == 2

# Test for the GET /embeddings/{id} endpoint
def test_get_embedding(client, mock_embedding_crud):
    # Prepare mock data for an embedding instance
    mock_embedding_instance = MagicMock()
    mock_embedding_instance.id = 1
    mock_embedding_instance.text = "This is some sample text."
    mock_embedding_instance.embedding = "0.1 0.2 0.3"

    mock_embedding_crud.get_embedding_by_id.return_value = (mock_embedding_instance, [0.1, 0.2, 0.3])

    # Make the GET request
    response = client.get("/embeddings/1")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "text": "This is some sample text.",
        "embedding": [0.1, 0.2, 0.3]
    }
    mock_embedding_crud.get_embedding_by_id.assert_called_once_with(mock_embedding_crud, 1)


# Test for the case when the embedding is not found
def test_get_embedding_not_found(client, mock_embedding_crud):
    # Make the GET request with a non-existing ID
    mock_embedding_crud.get_embedding_by_id.return_value = None
    response = client.get("/embeddings/999")  # ID 999 does not exist

    # Assertions
    assert response.status_code == 404
    assert response.json() == {"detail": "Embedding not found"}


# Test for the GET /embeddings/{id} endpoint
def test_get_embedding(client, mock_embedding_crud):
    # Prepare mock data for an embedding instance
    mock_embedding_instance = MagicMock()
    mock_embedding_instance.id = 1
    mock_embedding_instance.text = "This is some sample text."
    mock_embedding_instance.embedding = "0.1 0.2 0.3"

    mock_embedding_crud.get_embedding_by_id.return_value = (mock_embedding_instance, [0.1, 0.2, 0.3])

    # Make the GET request
    response = client.get("/embeddings/1")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "text": "This is some sample text.",
        "embedding": [0.1, 0.2, 0.3]
    }


# Test for the case when the embedding is not found
def test_get_embedding_not_found(client, mock_embedding_crud):
    # Make the GET request with a non-existing ID
    mock_embedding_crud.get_embedding_by_id.return_value = None
    response = client.get("/embeddings/999")  # ID 999 does not exist

    # Assertions
    assert response.status_code == 404
    assert response.json() == {"detail": "Embedding not found"}
