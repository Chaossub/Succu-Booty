import json
import os
import time
from pyrogram import filters
from handlers.utils import admin_only

WARN_FILE = "data/warns.json"

def load_warns():
    if os.path.exists(WARN_FILE):
        with open(WARN_FILE, "r") as f:
            return json.load(f)
    return {}

def save_warns(data):
    with open(WARN_FILE, "w") as f:
        json.dump(data, f, indent=2)

def register(app):
    @app.on_message(filters.command("warn") & filters.group)
    @admin_only
    async def warn_user(client, message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to warn them.")
            return
        user_id = str(message.reply_to_message.from_user.id)
        chat_id = str(message.chat.id)
        data = load_warns()
        data.setdefault(chat_id, {}).setdefault(user_id, 0)
        data[chat_id][user_id] += 1
        save_warns(data)
        warns = data[chat_id][user_id]
        await message.reply(f"Warned! Total warns: {warns}")
        if warns == 3:
            try:
                until = int(time.time()) + 5*60
                await client.restrict_chat_member(chat_id, int(user_id), permissions=None, until_date=until)
                await message.reply("Auto-mute: 5 minutes for 3 warns.")
            except Exception as e:
                await message.reply(f"Failed to mute: {e}")
        if warns == 6:
            try:
                until = int(time.time()) + 10*60
                await client.restrict_chat_member(chat_id, int(user_id), permissions=None, until_date=until)
                await message.reply("Auto-mute: 10 minutes for 6 warns.")
            except Exception as e:
                await message.reply(f"Failed to mute: {e}")

    @app.on_message(filters.command("resetwarns") & filters.group)
    @admin_only
    async def reset_warns(client, message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to reset their warns.")
            return
        user_id = str(message.reply_to_message.from_user.id)
        chat_id = str(message.chat.id)
        data = load_warns()
        data.setdefault(chat_id, {})[user_id] = 0
        save_warns(data)
        await message.reply("Warnings reset!")

    @app.on_message(filters.command("warns") & filters.group)
    async def warns(client, message):
        if message.reply_to_message:
            user_id = str(message.reply_to_message.from_user.id)
        else:
            args = message.text.split(maxsplit=1)
            if len(args) < 2:
                await message.reply("Reply or use /warns @username")
                return
            user = await client.get_users(args[1])
            user_id = str(user.id)
        chat_id = str(message.chat.id)
        data = load_warns()
        warns = data.get(chat_id, {}).get(user_id, 0)
        await message.reply(f"Warnings: {warns}")

    @app.on_message(filters.command("mute") & filters.group)
    @admin_only
    async def mute_user(client, message):
        if not message.reply_to_message:
            await message.reply("Reply to the user's message to mute them.")
            return
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        args = message.text.split()
        seconds = 0
        if len(args) > 1:
            try:
                seconds = int(args[1]) * 60
            except:
                seconds = 0
        until = int(time.time()) + (seconds if seconds else 60*60*24*365)
        try:
            await client.restrict_chat_member(chat_id, user_id, permissions=None, until_date=until)
            await message.reply("User has been muted.")
        except Exception as e:
            await message.reply(f"Failed to mute: {e}")

    @app.on_message(filters.command("unmute") & filters.group)
    @admin_only
    async def unmute_user(client, message):
        if not message.reply_to_message:
            await message.reply("Reply to the muted user's message to unmute them.")
            return
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        try:
            await client.unban_chat_member(chat_id, user_id)
            await message.reply("User has been unmuted.")
        except Exception as e:
            await message.reply(f"Failed to unmute: {e}")

    @app.on_message(filters.command("kick") & filters.group)
    @admin_only
    async def kick_user(client, message):
        if not message.reply_to_message:
            await message.reply("Reply to the user's message you want to kick.")
            return
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        try:
            await client.kick_chat_member(chat_id, user_id)
            await client.unban_chat_member(chat_id, user_id)
            await message.reply("User has been kicked from the group!")
        except Exception as e:
            await message.reply(f"Failed to kick: {e}")

    @app.on_message(filters.command("ban") & filters.group)
    @admin_only
    async def ban_user(client, message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to ban them.")
            return
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        try:
            await client.kick_chat_member(chat_id, user_id)
            await message.reply("User has been banned.")
        except Exception as e:
            await message.reply(f"Failed to ban: {e}")

    @app.on_message(filters.command("unban") & filters.group)
    @admin_only
    async def unban_user(client, message):
        if not message.reply_to_message:
            await message.reply("Reply to a user to unban them.")
            return
        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        try:
            await client.unban_chat_member(chat_id, user_id)
            await message.reply("User has been unbanned.")
        except Exception as e:
            await message.reply(f"Failed to unban: {e}")

    @app.on_message(filters.command("flirtywarn") & filters.group)
    @admin_only
    async def flirtywarn_user(client, message):
        FLIRTY_WARN_MSGS = [
            "Mmm, {mention}... that’s a naughty move, but I like your style.",
            "Careful, {mention}, you’re racking up the flirty warnings!",
            "One more slip and you’ll have the succubi’s full attention, {mention} 😉.",
            "Ooh, {mention}, you’re dancing on the edge. Flirty warning given!",
            "That was bold, {mention}. Don’t make me punish you... or do.",
        ]
        if not message.reply_to_message:
            await message.reply("Reply to a user to flirtywarn them.")
            return
        user = message.reply_to_message.from_user
        await message.reply(random.choice(FLIRTY_WARN_MSGS).format(mention=user.mention))

    @app.on_message(filters.command("cancel") & filters.group)
    async def cancel_cmd(client, message):
        await message.reply("Current operation canceled.")
