import os
import json
from pyrogram import filters
from handlers.utils import admin_only
from datetime import datetime, timezone

FLYERS_FILE = "data/flyers.json"

def load_flyers():
    if os.path.exists(FLYERS_FILE):
        with open(FLYERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_flyers(data):
    with open(FLYERS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def register(app):
    @app.on_message(filters.command("addflyer") & filters.group)
    @admin_only
    async def add_flyer(client, message):
        args = message.text.split(maxsplit=1)
        if len(args) < 2 or not message.reply_to_message or not message.reply_to_message.photo:
            await message.reply("Reply to an image with: /addflyer <name>")
            return
        name = args[1].strip().lower()
        flyers = load_flyers()
        chat_id = str(message.chat.id)
        file_id = message.reply_to_message.photo.file_id
        flyers.setdefault(chat_id, {})[name] = {"file_id": file_id}
        save_flyers(flyers)
        await message.reply(f"✅ Flyer '{name}' added.")

    @app.on_message(filters.command("listflyers") & filters.group)
    async def list_flyers(client, message):
        flyers = load_flyers()
        chat_id = str(message.chat.id)
        if chat_id not in flyers or not flyers[chat_id]:
            await message.reply("No flyers found.")
            return
        text = "📋 <b>Flyers in this group:</b>\n"
        text += "\n".join(f"• {name}" for name in flyers[chat_id])
        await message.reply(text)

    @app.on_message(filters.command("flyer") & filters.group)
    async def get_flyer(client, message):
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply("Usage: /flyer <name>")
            return
        name = args[1].strip().lower()
        flyers = load_flyers()
        chat_id = str(message.chat.id)
        if chat_id not in flyers or name not in flyers[chat_id]:
            await message.reply("No flyer with that name.")
            return
        await message.reply_photo(flyers[chat_id][name]["file_id"], caption=f"Flyer: {name}")

    @app.on_message(filters.command("changeflyer") & filters.group)
    @admin_only
    async def change_flyer(client, message):
        args = message.text.split(maxsplit=1)
        if len(args) < 2 or not message.reply_to_message or not message.reply_to_message.photo:
            await message.reply("Reply to a new image with: /changeflyer <name>")
            return
        name = args[1].strip().lower()
        flyers = load_flyers()
        chat_id = str(message.chat.id)
        if chat_id not in flyers or name not in flyers[chat_id]:
            await message.reply("No flyer with that name.")
            return
        file_id = message.reply_to_message.photo.file_id
        flyers[chat_id][name]["file_id"] = file_id
        save_flyers(flyers)
        await message.reply(f"✅ Flyer '{name}' updated.")

    @app.on_message(filters.command("deleteflyer") & filters.group)
    @admin_only
    async def delete_flyer(client, message):
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply("Usage: /deleteflyer <name>")
            return
        name = args[1].strip().lower()
        flyers = load_flyers()
        chat_id = str(message.chat.id)
        if chat_id not in flyers or name not in flyers[chat_id]:
            await message.reply("No flyer with that name.")
            return
        del flyers[chat_id][name]
        save_flyers(flyers)
        await message.reply(f"🗑️ Flyer '{name}' deleted.")

    @app.on_message(filters.command("scheduleflyer") & filters.group)
    @admin_only
    async def schedule_flyer(client, message):
        args = message.text.split(maxsplit=2)
        if len(args) < 3:
            await message.reply("Usage: /scheduleflyer <name> <YYYY-MM-DD HH:MM> (UTC)")
            return
        name = args[1].strip().lower()
        timestr = args[2].strip()
        try:
            send_time = datetime.strptime(timestr, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        except:
            await message.reply("Invalid date format. Use: YYYY-MM-DD HH:MM (UTC)")
            return
        flyers = load_flyers()
        chat_id = str(message.chat.id)
        if chat_id not in flyers or name not in flyers[chat_id]:
            await message.reply("No flyer with that name.")
            return
        flyers[chat_id][name]["scheduled"] = send_time.isoformat()
        save_flyers(flyers)
        await message.reply(f"✅ Flyer '{name}' scheduled for {send_time.strftime('%Y-%m-%d %H:%M UTC')}")

    async def flyer_scheduler(app):
        while True:
            now = datetime.now(timezone.utc)
            flyers = load_flyers()
            for chat_id, group_flyers in flyers.items():
                for name, flyer in group_flyers.items():
                    sched = flyer.get("scheduled")
                    if sched:
                        post_time = datetime.fromisoformat(sched)
                        if now >= post_time:
                            try:
                                await app.send_photo(int(chat_id), flyer["file_id"], caption=f"Scheduled flyer: {name}")
                            except Exception as e:
                                print(f"Error posting scheduled flyer: {e}")
                            del flyer["scheduled"]
                            save_flyers(flyers)
            await asyncio.sleep(60)

    # Register scheduler with main.py
    def register_scheduler(app):
        import asyncio
        asyncio.create_task(flyer_scheduler(app))
