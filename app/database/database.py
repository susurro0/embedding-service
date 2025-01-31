import os
from typing import List

from peewee import PostgresqlDatabase

from dotenv import load_dotenv

load_dotenv()
class Database:
    database: PostgresqlDatabase

    def __init__(self, db_path: str):
        """
        Initialize the Database class with a SQLite database file path.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.database = PostgresqlDatabase(db_path)

    def connect(self):
        """
        Connect to the database.
        """
        if self.database.is_closed():
            self.database.connect()

    def close(self):
        """
        Close the database connection.
        """
        if not self.database.is_closed():
            self.database.close()

    def create_tables(self, table_names: List):
        """
        Initialize the database by creating tables.
        """
        self.connect()
        self.database.create_tables(table_names, safe=True)
        self.close()

db_url = f"{os.getenv('DATABASE_URL')}"
database_instance = Database(db_url)