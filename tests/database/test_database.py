import pytest
from unittest.mock import patch, MagicMock

from app.database.database import Database


@pytest.fixture
def mock_database():
    """
    Fixture to create a mock database instance.
    """
    with patch("app.database.database.SqliteDatabase") as MockSqliteDatabase:
        mock_db_instance = MagicMock()
        MockSqliteDatabase.return_value = mock_db_instance
        yield mock_db_instance


def test_database_initialization(mock_database):
    """
    Test if the database is initialized with the correct path.
    """
    db_path = "test.db"
    db = Database(db_path=db_path)
    assert mock_database is db.db  # Ensure the database instance is correctly assigned


def test_database_connect(mock_database):
    """
    Test if the database connects when connect() is called.
    """
    db = Database()
    db.connect()
    mock_database.connect.assert_called_once()



def test_database_close(mock_database):
    """
    Test if the database closes when close() is called.
    """
    db = Database()
    db.db = mock_database  # Explicitly assign the mock database
    mock_database.is_closed.return_value = False  # Configure mock database
    db.close()
    mock_database.close.assert_called_once()

def test_database_initialize(mock_database):
    """
    Test if initialize() connects, creates tables, and closes the connection.
    """
    mock_table = MagicMock()
    db = Database()

    with patch.object(db, "connect") as mock_connect, \
         patch.object(db, "close") as mock_close, \
         patch.object(db.db, "create_tables") as mock_create_tables:

        db.initialize([mock_table])

        # Verify that the methods were called
        mock_connect.assert_called_once()
        mock_create_tables.assert_called_once_with([mock_table], safe=True)
        mock_close.assert_called_once()