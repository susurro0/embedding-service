from contextlib import contextmanager
from typing import Generator

from app.database.database import Database


class Dependency:
    def __init__(self, db: Database):
        """
        Dependency class to manage database interactions.

        Args:
            db (Database): An instance of the Database class.
        """
        self.db = db

    @contextmanager
    def get_db(self) -> Generator:
        """
        Provide a database connection for the duration of a request.

        Yields:
            Database.connection: An active database connection.
        """
        try:
            # Establish the connection
            self.db.connect()
            yield self.db.database
        finally:
            # Close the connection after use
            self.db.close()
