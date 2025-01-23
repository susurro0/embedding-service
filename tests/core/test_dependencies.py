import pytest
from unittest import mock
from app.database.database import Database
from app.core.dependencies import Dependency


@pytest.fixture
def mock_db_instance():
    # Mock the Database class
    mock_db = mock.Mock(spec=Database)
    mock_db.db = "mock_connection"
    return mock_db


def test_get_db_connects_and_yields(mock_db_instance):
    # Create Dependency instance with the mock database
    dependency = Dependency(mock_db_instance)

    # Use the mock `connect` and `close` methods
    with mock.patch.object(mock_db_instance, 'connect') as mock_connect, \
         mock.patch.object(mock_db_instance, 'close') as mock_close:

        # Call the get_db method
        with dependency.get_db() as db_conn:
            # Assert that the connection is established
            mock_connect.assert_called_once()
            assert db_conn == "mock_connection"

        # Ensure that close was called after use
        mock_close.assert_called_once()

def test_get_db_closes_connection(mock_db_instance):
    # Create Dependency instance with the mock database
    dependency = Dependency(mock_db_instance)

    # Mock the connection and close method
    with mock.patch.object(mock_db_instance, 'connect') as mock_connect, \
         mock.patch.object(mock_db_instance, 'close') as mock_close:

        # Use get_db() to ensure that close gets called
        with dependency.get_db():
            pass  # Just need to ensure it works without errors

        # Assert the connection is closed after use
        mock_close.assert_called_once()
