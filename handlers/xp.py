import json
import os
from pyrogram import filters

XP_FILE = "data/xp.json"

def load_xp():
    if os.path.exists(XP_FILE):
        with open(XP_FILE, "r") as f:
            return json.load(f)
    return {}

def save_xp(data):
    with open(XP_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_xp(chat_id, user_id, amount=1):
    chat_id = str(chat_id)
    user_id = str(user_id)
    data = load_xp()
    if chat_id not in data:
        data[chat_id] = {}
    if user_id not in data[chat_id]:
        data[chat_id][user_id] = 0
    data[chat_id][user_id] += amount
    save_xp(data)
    return data[chat_id][user_id]

def get_xp(chat_id, user_id):
    chat_id = str(chat_id)
    user_id = str(user_id)
    data = load_xp()
    return data.get(chat_id, {}).get(user_id, 0)

def register(app):
    @app.on_message(filters.command("naughty") & filters.group)
    async def naughty(client, message):
        user_id = message.from_user.id
        xp = get_xp(message.chat.id, user_id)
        await message.reply(f"Your naughty XP: {xp}")

    @app.on_message(filters.command("leaderboard") & filters.group)
    async def leaderboard(client, message):
        chat_id = str(message.chat.id)
        data = load_xp().get(chat_id, {})
        if not data:
            await message.reply("No naughty XP in this group yet.")
            return
        users = sorted(data.items(), key=lambda x: x[1], reverse=True)
        out = "<b>🔥 Succubus Sanctuary Naughty Leaderboard 🔥</b>\n"
        for i, (uid, xp) in enumerate(users[:10], 1):
            try:
                user = await client.get_users(int(uid))
                out += f"{i}. {user.mention} — {xp} XP\n"
            except Exception:
                out += f"{i}. <code>{uid}</code> — {xp} XP\n"
        await message.reply(out)
