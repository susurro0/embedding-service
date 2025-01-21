# initialize.py
from fastapi import FastAPI

from app.database.database import Database
from app.models.models import Embedding


class AppInitializer:
    def __init__(self, app: FastAPI, database: Database):
        self.app = app
        self.database = database

    def initialize(self):
        # Initialize database
        self.database.initialize([Embedding])
