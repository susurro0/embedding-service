# initialize.py
from fastapi import FastAPI

from app.database.database import Database
from app.models.embedding_model import Embedding


class AppInitializer:
    def __init__(self, app: FastAPI, db: Database):
        self.app = app
        self.db = db

    def initialize(self):
        # Initialize database
        self.app.state.database = self.db
        self.db.create_tables([Embedding])
