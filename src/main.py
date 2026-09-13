import asyncio
import logging
import os

from src.config import load_config
from src.state import load_state, save_state
from src.telegram_client import get_telegram_client
from src.telegram_source import fetch_new_videos
from src.keyword_research import get_keyword_suggestions
from src.metadata_generator import generate_video_metadata
from src.youtube_uploader import get_youtube_client, upload_video

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def build_description(description: str, hashtags: list[str]) -> str:
    if not hashtags:
        return description
    tag_line = " ".join(f"#{h.replace(' ', '')}" for h in hashtags)
    return f"{description}\n\n{tag_line}"


async def notify(client, chat, text: str) -> None:
    try:
        await client.send_message(chat, text)
    except Exception as e:
        logger.warning(f"Could not send Telegram notification: {e}")


async def main() -> None:
    config = load_config()
    state_path = config.get("paths", {}).get("state_file", "data/state.json")
    state = load_state(state_path)

    client = get_telegram_client(config)
    await client.start()

    try:
        max_per_run = config.get("limits", {}).get("max_uploads_per_run", 2)
        videos = await fetch_new_videos(client, config, state, limit=max_per_run)

        if not videos:
            logger.info("No new videos found.")
            return

        youtube = get_youtube_client(config)
        source_chat = config["telegram_source_chat"]
        max_keywords = config.get("keywords", {}).get("max_keywords", 15)
        category_id = config.get("youtube", {}).get("category_id", "22")
        privacy_status = config.get("youtube", {}).get("privacy_status", "public")

        for video in videos:
            topic = video["caption"] or "video"
            logger.info(f"Processing message {video['message_id']}: topic='{topic}'")
            try:
                keywords = await get_keyword_suggestions(topic, max_keywords=max_keywords)
                metadata = await generate_video_metadata(topic, keywords, config)
                description = build_description(metadata["description"], metadata["hashtags"])

                video_id = upload_video(
                    youtube,
                    video["file_path"],
                    metadata["title"],
                    description,
                    metadata["tags"],
                    category_id=category_id,
                    privacy_status=privacy_status,
                )

                url = f"https://youtu.be/{video_id}"
                logger.info(f"Uploaded: {url}")
                await notify(client, source_chat, f"✅ Uploaded to YouTube:\n{metadata['title']}\n{url}")

            except Exception as e:
                logger.error(f"Failed to process message {video['message_id']}: {e}")
                await notify(
                    client,
                    source_chat,
                    f"⚠️ Failed to publish video (message {video['message_id']}): {e}",
                )
            finally:
                if os.path.exists(video["file_path"]):
                    os.remove(video["file_path"])

    finally:
        save_state(state, state_path)
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
