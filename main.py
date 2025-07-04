import asyncio
import os
from pyrogram import Client
from handlers import (
    welcome,
    help_cmd,
    moderation,
    federation,
    summon,
    xp,
    fun,
    flyers,
    flirtydays,
)
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "SuccuBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

async def startup_tasks():
    print("Running startup tasks...")
    # Example: start flyer scheduler or flirtydays scheduler here
    # asyncio.create_task(flyers.flyer_scheduler(app))
    # asyncio.create_task(flirtydays.post_daily_flirty_theme(app))
    pass

async def main():
    await app.start()
    # Register all handlers
    welcome.register(app)
    help_cmd.register(app)
    moderation.register(app)
    federation.register(app)
    summon.register(app)
    xp.register(app)
    fun.register(app)
    flyers.register(app)
    flirtydays.register(app)

    await startup_tasks()

    print("SuccuBot is running...")
    await app.idle()  # Keep running until Ctrl+C or stop signal
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
