from typing import List, Tuple


def validates_scores(raw_scores: List[float]) -> List[float]:
    cleaned = []

    for s in raw_scores:
        if not isinstance(s, (int, float)):
            raise ValueError(f"Invalid score: {s} (not a number)")

        if s < 0 or s > 100:
            raise ValueError(f"Invalid score: {s} (must be 0–100)")
        cleaned.append(float(s))

    return cleaned


def mean(scores: List[float]) -> float:
    return sum(scores) / len(scores)


def min_max(scores: List[float]) -> Tuple[float, float]:
    return (min(scores), max(scores))


def letter_grade(avg: float) -> str:
    if avg >= 85:
        return "HD"
    elif avg >= 75:
        return "D"
    elif avg >= 65:
        return "C"
    elif avg >= 50:
        return "P"
    else:
        return "F"
