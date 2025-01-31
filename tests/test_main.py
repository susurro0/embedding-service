import pytest
from fastapi.testclient import TestClient
from unittest import mock

from app.main import create_app
from app.database.database import Database
from app.core.dependencies import Dependency
from app.api.endpoints import EmbeddingRoutes


# Mock objects for the dependencies
@pytest.fixture
def mock_database():
    return mock.Mock(spec=Database)


@pytest.fixture
def mock_dependency(mock_database):
    return Dependency(mock_database)


@pytest.fixture
def mock_embedding_crud():
    return mock.Mock()


@pytest.fixture
def test_client(mock_database, mock_dependency, mock_embedding_crud):
    # Mock EmbeddingRoutes to use mock dependencies
    with mock.patch("app.api.endpoints.EmbeddingRoutes", autospec=True) as MockEmbeddingRoutes:
        MockEmbeddingRoutes.return_value = mock.Mock(router="mock_router")

        # Initialize the app with mocks
        app = create_app()
        return TestClient(app)


def test_app_initialization(test_client):
    """
    Test that the FastAPI app initializes correctly.
    """
    response = test_client.get("/")
    assert response.status_code == 404  # "/" is not defined in this app by default


def test_cors_middleware(test_client):
    """
    Test CORS middleware settings.
    """
    headers = {
        "Origin": "http://localhost:5174",
    }
    response = test_client.options("/", headers=headers)
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:5174"


def test_routes_included(mock_dependency, mock_embedding_crud):
    """
    Test that routes are correctly included.
    """

    app = create_app()
    routes = app.router.routes

    expected_routes = {
        "create_embedding_from_text": "/embedding/text/",
        "get_embedding": "/embeddings/{id}"
    }

    # Check if routes exist with correct paths
    for name, path in expected_routes.items():
        matching_route = next((route for route in routes if route.name == name), None)
        assert matching_route is not None, f"Route with name '{name}' not found"
        assert matching_route.path == path, f"Route path mismatch for '{name}'"


def test_dependency_initialization(mock_database):
    """
    Test that Dependency is initialized with the Database instance.
    """
    dependency = Dependency(mock_database)
    assert dependency.db == mock_database
