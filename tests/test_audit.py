import json
import sqlite3

from adiuvare.core.models import AdiuvareEvent
from adiuvare.state.audit_log import AuditLog


def test_audit_log_writes_event(tmp_path):
    db_path = tmp_path / "audit.db"
    log = AuditLog(db_path)
    event = AdiuvareEvent(
        identity="u1",
        endpoint="/login",
        score=0.42,
        verdict="flag",
        breakdown={"payload": 0.28, "identity": 0.14},
    )

    log.write(event)

    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "select identity, verdict, breakdown_json from audit_events"
        ).fetchone()

    assert row is not None
    assert row[0] == "u1"
    assert row[1] == "flag"
    assert json.loads(row[2])["payload"] == 0.28
