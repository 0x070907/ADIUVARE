import sqlite3
from pathlib import Path

from .identity_store import IdentityStore


def init_state_db(db_path: str | Path) -> None:
    schema = Path(__file__).with_name("schema.sql").read_text()
    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema)


def save_identity_state(db_path: str | Path, id_store: IdentityStore) -> None:
    with sqlite3.connect(db_path) as conn:
        for identity, win in id_store._windows.items():
            conn.execute(
                """
                insert or replace into identity_state (
                    identity,
                    seen,
                    score_ewma,
                    blocked_until
                ) values (?, ?, ?, ?)
                """,
                (identity, win.seen, win.score_ewma, win.blocked_until),
            )
        conn.commit()
