# agent.py
from tools import simple_search

SHORT_MEMORY = []
MAX_MEMORY_ITEMS = 10

def _push_memory(role: str, text: str) -> None:
    if SHORT_MEMORY and SHORT_MEMORY[-1].get("role") == role and SHORT_MEMORY[-1].get("text") == text:
        return
    SHORT_MEMORY.append({"role": role, "text": text})
    while len(SHORT_MEMORY) > MAX_MEMORY_ITEMS:
        SHORT_MEMORY.pop(0)

def is_factual(query: str) -> bool:
    if not query:
        return False
    q = query.strip().lower()
    if q.startswith(("what", "who", "when", "where", "why", "how", "which")) or "?" in q:
        return True
    keywords = ["capital", "invent", "year", "date", "population", "largest", "speed", "boiling", "how many", "how much"]
    return any(k in q for k in keywords)

def agent_response(user_msg: str) -> dict:
    user_msg = (user_msg or "").strip()
    _push_memory("user", user_msg)

    if is_factual(user_msg):
        answer, score = simple_search(user_msg)
        if answer and score >= 0.60:
            _push_memory("agent", answer)
            return {"type": "factual", "answer": answer, "memory": list(SHORT_MEMORY), "confidence": round(score, 2)}
        else:
            fallback = "I don't have that fact in my small database. Try a different question or check a reference."
            _push_memory("agent", fallback)
            return {"type": "factual", "answer": fallback, "memory": list(SHORT_MEMORY), "confidence": round(score, 2)}
    else:
        reply = "Thanks for that! I'm a small helper — I can answer simple factual questions or chat briefly."
        _push_memory("agent", reply)
        return {"type": "conversational", "answer": reply, "memory": list(SHORT_MEMORY)}
