from ..core.models import SignalResult

_weights = {
    "payload": 0.40,
    "behavior": 0.35,
    "identity": 0.25,
}


def compute_score(sig_res: dict[str, SignalResult]) -> tuple[float, dict[str, float]]:
    breakdown: dict[str, float] = {}
    total = 0.0

    for name, res in sig_res.items():
        weight = _weights.get(name, 0.0)
        part = res.score * weight
        breakdown[name] = part
        total += part

    return min(total, 1.0), breakdown

