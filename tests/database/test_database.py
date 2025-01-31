import pytest
from unittest.mock import patch, MagicMock
from app.database.database import Database


@pytest.fixture
def mock_database():
    """
    Fixture to create a mock database instance.
    """
    with patch("app.database.database.PostgresqlDatabase") as MockPostgresqlDatabase:
        mock_db_instance = MagicMock()
        MockPostgresqlDatabase.return_value = mock_db_instance
        yield mock_db_instance


def test_database_initialization(mock_database):
    """
    Test if the database is initialized with the correct connection.
    """
    db_path = "test_db"
    db = Database(db_path=db_path)

    # Ensure the database instance is correctly assigned
    assert isinstance(db.database, MagicMock)  # Mock should be assigned
    assert db.database == mock_database  # Check mock assignment


def test_database_connect(mock_database):
    """
    Test if the database connects when connect() is called.
    """
    db = Database('test_db')
    db.connect()
    mock_database.connect.assert_called_once()


def test_database_close(mock_database):
    """
    Test if the database closes when close() is called.
    """
    db = Database('test_db')
    db.database = mock_database  # Assign the mock database explicitly
    mock_database.is_closed.return_value = False  # Simulate open database
    db.close()
    mock_database.close.assert_called_once()


def test_database_initialize(mock_database):
    """
    Test if initialize() connects, creates tables, and closes the connection.
    """
    mock_table = MagicMock()
    db = Database('test_db')

    with patch.object(db, "connect") as mock_connect, \
            patch.object(db, "close") as mock_close, \
            patch.object(db.database, "create_tables") as mock_create_tables:
        db.create_tables([mock_table])

        # Verify that the methods were called
        mock_connect.assert_called_once()
        mock_create_tables.assert_called_once_with([mock_table], safe=True)
        mock_close.assert_called_once()
