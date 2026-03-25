def compute_verdict(score: float) -> str:
    if score >= 0.80:
        return "block"

    if score >= 0.55:
        return "throttle"

    if score >= 0.25:
        return "flag"

    return "allow"

