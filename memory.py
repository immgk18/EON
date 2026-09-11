"""
EON Memory
==========
Persistent memory system using SQLite.
"""

import sqlite3
from datetime import datetime


class Memory:
    """Stores and retrieves EON memories."""

    def __init__(self, database="eon.db"):
        self.database = database
        self._initialize()

    def _connect(self):
        """Create a database connection."""
        return sqlite3.connect(self.database)

    def _initialize(self):
        """Create the memory table if it doesn't exist."""

        connection = self._connect()

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()

    def remember(self, content, category="general"):
        """Store a new memory."""

        if not content:
            return False

        connection = self._connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO memories
            (category, content, created_at)
            VALUES (?, ?, ?)
            """,
            (
                category,
                content,
                datetime.now().isoformat()
            )
        )

        connection.commit()
        connection.close()

        return True

    def recall(self, keyword=None, limit=10):
        """Retrieve memories."""

        connection = self._connect()
        cursor = connection.cursor()

        if keyword:
            cursor.execute(
                """
                SELECT id, category, content, created_at
                FROM memories
                WHERE content LIKE ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (
                    f"%{keyword}%",
                    limit
                )
            )
        else:
            cursor.execute(
                """
                SELECT id, category, content, created_at
                FROM memories
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,)
            )

        results = cursor.fetchall()

        connection.close()

        return results

    def forget(self, memory_id):
        """Delete a specific memory."""

        connection = self._connect()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM memories WHERE id = ?",
            (memory_id,)
        )

        deleted = cursor.rowcount > 0

        connection.commit()
        connection.close()

        return deleted

    def clear(self):
        """Clear all stored memories."""

        connection = self._connect()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM memories")

        connection.commit()
        connection.close()

    def count(self):
        """Return the number of stored memories."""

        connection = self._connect()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM memories")

        result = cursor.fetchone()[0]

        connection.close()

        return result

    def status(self):
        """Return memory system status."""

        return {
            "database": self.database,
            "memories": self.count(),
            "status": "ONLINE"
        }
