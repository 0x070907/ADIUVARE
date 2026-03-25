from adiuvare.core.models import SignalResult
from adiuvare.core.scorer import compute_score
from adiuvare.core.verdict import compute_verdict


def test_score_uses_hardcoded_weights():
    score, breakdown = compute_score(
        {
            "payload": SignalResult(score=0.7, reason="sql_hit"),
            "behavior": SignalResult(score=0.3, reason="odd_ua"),
        }
    )

    assert round(score, 3) == 0.385
    assert round(breakdown["payload"], 3) == 0.28


def test_verdict_maps_score_ranges():
    assert compute_verdict(0.10) == "allow"
    assert compute_verdict(0.30) == "flag"
    assert compute_verdict(0.60) == "throttle"
    assert compute_verdict(0.90) == "block"

