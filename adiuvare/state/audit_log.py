import json
import sqlite3
from pathlib import Path

from ..core.models import AdiuvareEvent


class AuditLog:
    def __init__(self, db_path: str | Path) -> None:
        self._db_path = str(db_path)
        self._init_db()

    def _init_db(self) -> None:
        schema = Path(__file__).with_name("schema.sql").read_text()
        with sqlite3.connect(self._db_path) as conn:
            conn.executescript(schema)

    def write(self, event: AdiuvareEvent) -> None:
        row = (
            event.identity,
            event.endpoint,
            event.score,
            event.verdict,
            json.dumps(event.breakdown),
        )
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                """
                insert into audit_events (
                    identity,
                    endpoint,
                    score,
                    verdict,
                    breakdown_json
                ) values (?, ?, ?, ?, ?)
                """,
                row,
            )
            conn.commit()
