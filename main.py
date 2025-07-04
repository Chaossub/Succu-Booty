import asyncio
import os
import logging
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

logging.basicConfig(level=logging.INFO)  # or DEBUG for more verbosity

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
    while True:
        print("SuccuBot heartbeat - alive and kicking!")
        await asyncio.sleep(300)  # Every 5 minutes

async def main():
    try:
        await app.start()

        welcome.register(app)
        help_cmd.register(app)
        moderation.register(app)
        federation.register(app)
        summon.register(app)
        xp.register(app)
        fun.register(app)
        flyers.register(app)
        flirtydays.register(app)

        # Start heartbeat loop so container knows bot is alive
        asyncio.create_task(startup_tasks())

        print("SuccuBot is running...")
        await idle()  # Keeps bot running until CTRL+C
        await app.stop()

    except Exception as e:
        logging.error(f"Exception during startup or runtime: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())

