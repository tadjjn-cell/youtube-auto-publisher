import json
import logging

from src.config import get_groq_client, call_groq_with_retry

logger = logging.getLogger(__name__)


async def generate_video_metadata(
    topic: str, keywords: list[str], trending_queries: list[str], config: dict
) -> dict:
    """Call Groq (free tier) to turn a topic + keyword/trend signals into YouTube metadata."""
    client = get_groq_client(config)
    model = config.get("ai", {}).get("text_model", "openai/gpt-oss-120b")
    keywords_str = ", ".join(keywords) if keywords else "(none found)"
    trending_str = ", ".join(trending_queries) if trending_queries else "(none found)"

    response_text = await call_groq_with_retry(
        client,
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a YouTube growth/SEO expert who optimizes for click-through rate and "
                    "current search trends, without ever misleading the viewer. Return ONLY valid JSON."
                ),
            },
            {
                "role": "user",
                "content": f"""Generate YouTube video metadata for a video about: "{topic}"

Related search terms people actually type on YouTube: {keywords_str}
Currently trending/rising search queries around this topic (Google Trends, last 7 days): {trending_str}

Priorities:
1. Prefer wording from the TRENDING queries over the generic related terms whenever it fits the video naturally -- these get more current search volume.
2. The title must be the kind that makes people stop scrolling and click: strong hook, most important keyword near the start, numbers/specificity when relevant. No clickbait lies -- it must match what the video actually shows.
3. Hashtags should mix a couple of broad high-reach tags for this content category with specific niche/trending tags -- not just niche-only.

Return JSON with these exact keys:
- title: max 100 characters
- description: 150-400 words. First 2 lines must work as a standalone hook (shown before "Show more"). Naturally weave in the trending/related terms. End with a short call-to-action to like, comment, and subscribe.
- tags: a list of 15-25 short SEO tags/keywords for the YouTube tags field (no # symbol), trending terms first
- hashtags: a list of 10-15 hashtags (no # symbol, code will add it), broad reach tags first then niche/trending ones""",
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
