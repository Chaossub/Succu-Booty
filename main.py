import asyncio
import os
from pyrogram import Client, idle
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
    # Example: start background tasks here
    # asyncio.create_task(flyers.flyer_scheduler(app))
    # asyncio.create_task(flirtydays.post_daily_flirty_theme(app))
    pass

async def main():
    await app.start()

    # Register handlers after starting app
    welcome.register(app)
    help_cmd.register(app)
    moderation.register(app)
    federation.register(app)
    summon.register(app)
    xp.register(app)
    fun.register(app)
    flyers.register(app)

