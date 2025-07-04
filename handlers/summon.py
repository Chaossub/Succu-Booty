import json
import os
import random
from pyrogram import filters
from handlers.utils import admin_only

TRACKED_FILE = "data/tracked_users.json"

def load_tracked():
    if os.path.exists(TRACKED_FILE):
        with open(TRACKED_FILE, "r") as f:
            return json.load(f)
    return {}

def save_tracked(data):
    with open(TRACKED_FILE, "w") as f:
        json.dump(data, f, indent=2)

SUMMON_MESSAGES = [
    "{mention}, you’re being summoned to the party. Don’t make us come find you...",
    "Attention, {mention}! The succubi want you in the chat—now.",
    "Wake up, {mention}! It’s your turn for a little attention.",
    "👠 {mention}, stop lurking and let us spoil you.",
    "🔥 The fun can’t start without you, {mention}!",
    "{mention}, the Sanctuary misses your energy. Get in here!",
    "😈 {mention}, a succubus is whispering your name...",
    "{mention}, you’ve been summoned by temptation itself.",
    "💦 Don’t leave us waiting, {mention}. Come play!",
    "{mention}, you’ve officially been summoned. Naughty time starts now.",
]

FLIRTY_SUMMON_MESSAGES = [
    "Hey {mention}, one of the succubi is craving your company... care to indulge?",
    "Ooo, {mention}—the girls want to play with you tonight!",
    "{mention}, why don’t you join us for a little wicked fun?",
    "Succubus Alert! {mention}, you’ve been flirtily summoned. Hope you can keep up.",
    "{mention}, the ladies have a surprise for you. Enter at your own risk 😘",
    "Pssst, {mention}... someone here can’t stop thinking about you.",
    "{mention}, come closer—we don’t bite... unless you ask nicely.",
    "All eyes on you, {mention}. Let’s get naughty.",
    "{mention}, don’t leave the succubi waiting. They get restless when teased.",
    "Flirty summon for {mention}! Ready for a little temptation?",
]

def register(app):
    @app.on_message(filters.command("summon") & filters.group)
    async def summon(client, message):
        args = message.text.split()
        if len(args) > 1:
            if args[1].startswith("@"):
                user = await client.get_users(args[1])
                mention = user.mention
            else:
                await message.reply("Tag a user with @ or reply to their message.")
                return
            msg = random.choice(SUMMON_MESSAGES).format(mention=mention)
            await message.reply(msg)
        elif message.reply_to_message:
            user = message.reply_to_message.from_user
            mention = user.mention
            msg = random.choice(SUMMON_MESSAGES).format(mention=mention)
            await message.reply(msg)
        else:
            await message.reply("Tag a user with @ or reply to their message to summon them.")

    @app.on_message(filters.command("flirtysummon") & filters.group)
    async def flirtysummon(client, message):
        args = message.text.split()
        if len(args) > 1:
            if args[1].startswith("@"):
                user = await client.get_users(args[1])
                mention = user.mention
            else:
                await message.reply("Tag a user with @ or reply to their message.")
                return
            msg = random.choice(FLIRTY_SUMMON_MESSAGES).format(mention=mention)
            await message.reply(msg)
        elif message.reply_to_message:
            user = message.reply_to_message.from_user
            mention = user.mention
            msg = random.choice(FLIRTY_SUMMON_MESSAGES).format(mention=mention)
            await message.reply(msg)
        else:
            await message.reply("Tag a user with @ or reply to their message to flirty summon them.")

    @app.on_message(filters.command("summonall") & filters.group)
    async def summonall(client, message):
        chat_id = str(message.chat.id)
        tracked = load_tracked().get(chat_id, [])
        if not tracked:
            await message.reply("No users tracked yet! Use /trackall first.")
            return
        text = " ".join([f"<a href='tg://user?id={uid}'>summoned</a>" for uid in tracked])
        msg = random.choice(SUMMON_MESSAGES).replace("{mention}", text)
        await message.reply(msg, parse_mode="html")

    @app.on_message(filters.command("flirtysummonall") & filters.group)
    async def flirtysummonall(client, message):
        chat_id = str(message.chat.id)
        tracked = load_tracked().get(chat_id, [])
        if not tracked:
            await message.reply("No users tracked yet! Use /trackall first.")
            return
        text = " ".join([f"<a href='tg://user?id={uid}'>summoned</a>" for uid in tracked])
        msg = random.choice(FLIRTY_SUMMON_MESSAGES).replace("{mention}", text)
        await message.reply(msg, parse_mode="html")

    @app.on_message(filters.command("trackall") & filters.group)
    @admin_only
    async def trackall(client, message):
        chat_id = str(message.chat.id)
        tracked = load_tracked()
        tracked.setdefault(chat_id, [])
        async for member in client.get_chat_members(chat_id):
            if member.user.is_bot:
                continue
            if member.user.id not in tracked[chat_id]:
                tracked[chat_id].append(member.user.id)
        save_tracked(tracked)
        await message.reply("Tracked all current group members!")
