import pytest
from unittest.mock import Mock
from fastapi import FastAPI

from core.initializer import AppInitializer
from database.database import Database
from models.models import Embedding


@pytest.fixture
def mock_app():
    return FastAPI()


@pytest.fixture
def mock_database():
    return Mock(spec=Database)


def test_app_initializer_initialization(mock_app, mock_database):
    initializer = AppInitializer(app=mock_app, database=mock_database)
    assert initializer.app == mock_app
    assert initializer.database == mock_database


def test_app_initializer_initialize_calls_database_initialize(mock_app, mock_database):
    initializer = AppInitializer(app=mock_app, database=mock_database)
    initializer.initialize()
    mock_database.initialize.assert_called_once()
