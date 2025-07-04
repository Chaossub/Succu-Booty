import os
from pyrogram import filters
from handlers.session import (
    start_session,
    get_session,
    set_session_step,
    set_session_data,
    end_session,
)
from handlers.utils import admin_only, OWNER_ID
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["SuccubusSanctuary"]
feds = db["federations"]


def get_fed_by_group(chat_id):
    return feds.find_one({"groups": chat_id}) or feds.find_one({"_id": str(chat_id)})


def is_fed_admin(user_id, fed):
    return user_id == fed["owner"] or user_id in fed.get("admins", [])


def register(app):
    # Multi-step /createfed with cancel support
    @app.on_message(filters.command("createfed") & filters.group)
    @admin_only
    async def createfed_start(client, message):
        if get_fed_by_group(message.chat.id):
            await message.reply("❌ This group is already part of a federation.")
            return
        start_session(message.chat.id, message.from_user.id, "createfed")
        await message.reply(
            "Let's create a new federation!\nWhat should the federation's name be?\n\n(Send the name, or /cancel to abort.)"
        )

    @app.on_message(filters.text & filters.group)
    async def createfed_steps(client, message):
        session = get_session(message.chat.id, message.from_user.id)
        if not session or session["flow"] != "createfed":
            return
        step = session["step"]

        if step == 1:
            set_session_data(message.chat.id, message.from_user.id, "name", message.text.strip())
            set_session_step(message.chat.id, message.from_user.id, 2)
            await message.reply(
                "Great! Now send a description for your fe

