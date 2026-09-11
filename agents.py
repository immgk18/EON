"""
EON Memory
==========
Persistent intelligent memory system using SQLite.

Memory types:
- Preference
- Project
- Fact
- Instruction
- General

The system supports:
- Saving memories
- Searching memories
- Retrieving recent memories
- Categorization
- Updating memories
- Forgetting individual memories
- Clearing memories
"""


import sqlite3
from datetime import datetime


class Memory:
    """Persistent memory manager for EON."""

    VALID_CATEGORIES = {
        "preference",
        "project",
        "fact",
        "instruction",
        "general",
    }

    def __init__(self, database="eon.db"):

        self.database = database

        self._initialize()

    # =========================================================
    # DATABASE CONNECTION
    # =========================================================

    def _connect(self):

        return sqlite3.connect(
            self.database
        )

    # =========================================================
    # INITIALIZE DATABASE
    # =========================================================

    def _initialize(self):

        connection = self._connect()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT
            )
        """)

        connection.commit()
        connection.close()

    # =========================================================
    # SAVE MEMORY
    # =========================================================

    def remember(
        self,
        content,
        category="general"
    ):
        """Store a new long-term memory."""

        if not content:
            return False

        category = (
            category.lower().strip()
        )

        if category not in self.VALID_CATEGORIES:

            category = "general"

        now = datetime.now().isoformat()

        connection = self._connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO memories
            (
                category,
                content,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                category,
                content.strip(),
                now,
                now,
            )
        )

        connection.commit()
        connection.close()

        return True

    # =========================================================
    # SEARCH MEMORY
    # =========================================================

    def recall(
        self,
        keyword=None,
        category=None,
        limit=10
    ):
        """Retrieve relevant memories."""

        connection = self._connect()
        cursor = connection.cursor()

        if keyword and category:

            cursor.execute(
                """
                SELECT
                    id,
                    category,
                    content,
                    created_at,
                    updated_at
                FROM memories
                WHERE content LIKE ?
                AND category = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (
                    f"%{keyword}%",
                    category,
                    limit,
                )
            )

        elif keyword:

            cursor.execute(
                """
                SELECT
                    id,
                    category,
                    content,
                    created_at,
                    updated_at
                FROM memories
                WHERE content LIKE ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (
                    f"%{keyword}%",
                    limit,
                )
            )

        elif category:

            cursor.execute(
                """
                SELECT
                    id,
                    category,
                    content,
                    created_at,
                    updated_at
                FROM memories
                WHERE category = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (
                    category,
                    limit,
                )
            )

        else:

            cursor.execute(
                """
                SELECT
                    id,
                    category,
                    content,
                    created_at,
                    updated_at
                FROM memories
                ORDER BY id DESC
                LIMIT ?
                """,
                (
                    limit,
                )
            )

        results = cursor.fetchall()

        connection.close()

        return results

    # =========================================================
    # RELEVANT MEMORY
    # =========================================================

    def relevant(
        self,
        query,
        limit=5
    ):
        """
        Find memories relevant to a query.

        A lightweight keyword-based retrieval system
        is used for now. Semantic/vector retrieval can
        be added later.
        """

        if not query:
            return []

        words = [
            word.strip(
                ".,!?;:"
            ).lower()
            for word in query.split()
        ]

        words = [
            word
            for word in words
            if len(word) > 2
        ]

        if not words:
            return []

        results = []

        for word in words:

            memories = self.recall(
                keyword=word,
                limit=limit
            )

            for memory in memories:

                if memory not in results:

                    results.append(
                        memory
                    )

                if len(results) >= limit:

                    return results

        return results

    # =========================================================
    # GET MEMORY
    # =========================================================

    def get(self, memory_id):

        connection = self._connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                category,
                content,
                created_at,
                updated_at
            FROM memories
            WHERE id = ?
            """,
            (
                memory_id,
            )
        )

        result = cursor.fetchone()

        connection.close()

        return result

    # =========================================================
    # UPDATE MEMORY
    # =========================================================

    def update(
        self,
        memory_id,
        content=None,
        category=None
    ):
        """Update an existing memory."""

        existing = self.get(
            memory_id
        )

        if existing is None:
            return False

        new_content = (
            content
            if content
            else existing[2]
        )

        new_category = (
            category
            if category
            else existing[1]
        )

        new_category = (
            new_category
            .lower()
            .strip()
        )

        if new_category not in self.VALID_CATEGORIES:

            new_category = "general"

        connection = self._connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE memories
            SET
                category = ?,
                content = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                new_category,
                new_content.strip(),
                datetime.now().isoformat(),
                memory_id,
            )
        )

        connection.commit()

        updated = (
            cursor.rowcount > 0
        )

        connection.close()

        return updated

    # =========================================================
    # FORGET ONE MEMORY
    # =========================================================

    def forget(self, memory_id):

        connection = self._connect()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM memories
            WHERE id = ?
            """,
            (
                memory_id,
            )
        )

        deleted = (
            cursor.rowcount > 0
        )

        connection.commit()
        connection.close()

        return deleted

    # =========================================================
    # CLEAR MEMORY
    # =========================================================

    def clear(self):

        connection = self._connect()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM memories"
        )

        connection.commit()
        connection.close()

    # =========================================================
    # COUNT
    # =========================================================

    def count(self):

        connection = self._connect()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM memories"
        )

        result = cursor.fetchone()[0]

        connection.close()

        return result

    # =========================================================
    # CATEGORIES
    # =========================================================

    def categories(self):

        return sorted(
            self.VALID_CATEGORIES
        )

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):

        return {
            "database":
                self.database,

            "memories":
                self.count(),

            "categories":
                self.categories(),

            "status":
                "ONLINE",
        }
