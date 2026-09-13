import json
import logging

from src.config import get_groq_client, call_groq_with_retry

logger = logging.getLogger(__name__)


async def generate_video_metadata(topic: str, keywords: list[str], config: dict) -> dict:
    """Call Groq (free tier) to turn a topic + keyword list into YouTube metadata."""
    client = get_groq_client(config)
    model = config.get("ai", {}).get("text_model", "openai/gpt-oss-120b")
    keywords_str = ", ".join(keywords) if keywords else "(none found)"

    response_text = await call_groq_with_retry(
        client,
        model=model,
        messages=[
            {"role": "system", "content": "You are a YouTube SEO expert. Return ONLY valid JSON."},
            {
                "role": "user",
                "content": f"""Generate YouTube video metadata for a video about: "{topic}"
Related search terms people actually type on YouTube: {keywords_str}

Return JSON with these exact keys:
- title: max 100 characters, most important keyword near the start, curiosity-driven but honest (no clickbait lies)
- description: 150-400 words. First 2 lines must work as a standalone hook (shown before "Show more"). Naturally weave in the keywords. End with a short call-to-action to like, comment, and subscribe.
- tags: a list of 15-25 short SEO tags/keywords for the YouTube tags field (no # symbol)
- hashtags: a list of 10-15 hashtags (no # symbol, code will add it) relevant to the topic""",
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=2048,
        reasoning_effort="low",
    )

    data = json.loads(response_text)

    return {
        "title": data["title"][:100],
        "description": data["description"][:5000],
        "tags": [str(t) for t in data.get("tags", [])][:25],
        "hashtags": [str(h) for h in data.get("hashtags", [])][:15],
    }
