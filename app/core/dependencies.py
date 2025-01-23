from contextlib import contextmanager
from typing import Generator

from app.database.database import Database


class Dependency:
    def __init__(self, db_instance: Database):
        """
        Dependency class to manage database interactions.

        Args:
            db (Database): An instance of the Database class.
        """
        self.db_instance = db_instance

    @contextmanager
    def get_db(self) -> Generator:
        """
        Provide a database connection for the duration of a request.

        Yields:
            Database.connection: An active database connection.
        """
        try:
            # Establish the connection
            self.db_instance.connect()
            yield self.db_instance.db
        finally:
            # Close the connection after use
            self.db_instance.close()
