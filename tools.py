# tools.py
"""
Improved small search: returns (answer, score) where score is 0..1 confidence.
We use difflib to find the closest key (string similarity) and also check
token overlap to be safer.
"""
from difflib import SequenceMatcher

SMALL_DB = {
    "what is the capital of france": "Paris.",
    "who invented the telephone": "Alexander Graham Bell.",
    "what is the boiling point of water": "100°C (at 1 atm).",
    "what is the largest planet": "Jupiter.",
    "when did world war 2 end": "1945.",
    "what is the capital of india": "New Delhi.",
    "who discovered penicillin": "Alexander Fleming.",
    "what is the speed of light": "Approximately 299,792 km/s.",
    "how many continents are there": "Seven.",
    "what is 2 + 2": "4.",
}

def _normalize(s: str) -> str:
    return " ".join(s.lower().strip().split())

def _token_overlap(q: str, key: str) -> float:
    qset = set(q.split())
    kset = set(key.split())
    if not kset:
        return 0.0
    overlap = qset & kset
    return len(overlap) / max(1, len(kset))

def simple_search(query: str):
    """
    Return (answer, score) or (None, 0.0)
    score is in 0..1: higher is better confidence.
    """
    if not query:
        return None, 0.0
    q = _normalize(query)

    if q in SMALL_DB:
        return SMALL_DB[q], 1.0

    best_key = None
    best_ratio = 0.0
    for k in SMALL_DB.keys():
        ratio = SequenceMatcher(None, q, k).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_key = k

    overlap = _token_overlap(q, best_key) if best_key else 0.0

    score = 0.6 * best_ratio + 0.4 * overlap

    if best_key:
        return SMALL_DB[best_key], float(score)
    return None, 0.0
