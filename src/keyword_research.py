import logging

import httpx

logger = logging.getLogger(__name__)

SUGGEST_URL = "https://suggestqueries.google.com/complete/search"


async def get_keyword_suggestions(topic: str, max_keywords: int = 15) -> list[str]:
    """
    Free YouTube keyword research using YouTube's own public autocomplete endpoint.
    No API key required. Widens the topic with a few common search-intent prefixes.
    """
    if not topic:
        return []

    queries = [topic, f"{topic} tips", f"{topic} tutorial", f"how to {topic}", f"best {topic}"]
    suggestions: list[str] = []

    async with httpx.AsyncClient(timeout=10) as client:
        for q in queries:
            try:
                resp = await client.get(SUGGEST_URL, params={"client": "firefox", "ds": "yt", "q": q})
                resp.raise_for_status()
                data = resp.json()
                suggestions.extend(data[1])
            except Exception as e:
                logger.warning(f"Keyword suggestion request failed for '{q}': {e}")
                continue

    seen = set()
    unique: list[str] = []
    for s in suggestions:
        s_clean = s.strip()
        key = s_clean.lower()
        if key and key not in seen:
            seen.add(key)
            unique.append(s_clean)

    return unique[:max_keywords]
