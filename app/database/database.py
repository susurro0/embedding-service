from typing import List

from peewee import SqliteDatabase


class Database:
    db: SqliteDatabase

    def __init__(self, db_path: str = "embeddings.db"):
        """
        Initialize the Database class with a SQLite database file path.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db = SqliteDatabase(db_path)

    def connect(self):
        """
        Connect to the database.
        """
        if self.db.is_closed():
            self.db.connect()

    def close(self):
        """
        Close the database connection.
        """
        if not self.db.is_closed():
            self.db.close()

    def initialize(self, table_names: List):
        """
        Initialize the database by creating tables.
        """
        self.connect()
        self.db.create_tables(table_names, safe=True)
        self.close()
