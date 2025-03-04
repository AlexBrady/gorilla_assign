"""Base Persistor class for DB operations."""

from metr.database.database import Session


class BasePersistor:
    """Base class for all persistors to handle session management."""

    def __init__(self):
        self.session = Session()

    def commit(self):
        """Commit transaction."""
        self.session.commit()

    def rollback(self):
        """Rollback transaction."""
        self.session.rollback()

    def close(self):
        """Close session."""
        self.session.close()
