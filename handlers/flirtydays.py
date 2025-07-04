import asyncio
from datetime import datetime, timezone
from pyrogram import filters

FLIRTY_THEMES = {
    0: (
        "Moan-day Madness",
        "🔥 <b>Moan-day Madness</b> 🔥\n"
        "Start your week with a little mischief! Today the succubi are ready to tease, tempt, and moan just for you. Ask for extra attention or start a playful challenge—Moan-day is all about letting your desires be heard!"
    ),
    1: (
        "Temptation Tuesday",
        "💋 <b>Temptation Tuesday</b> 💋\n"
        "Our succubi are turning up the temptation! Expect flirty dares, wicked games, and maybe a few secrets whispered in your ear. Don’t hold back—let the temptations begin!"
    ),
    2: (
        "Wicked Wednesday",
        "😈 <b>Wicked Wednesday</b> 😈\n"
        "Double trouble is on the menu! Succubi will team up for playful double-teases and group games. Tag a friend and see who can handle the most wicked fun!"
    ),
    3: (
        "Thirsty Thursday",
        "💦 <b>Thirsty Thursday</b> 💦\n"
        "The succubi are feeling extra thirsty—and they’re not talking about water. Request a flirty compliment, a saucy dare, or share your own thirstiest line for a special surprise!"
    ),
    4: (
        "Flirty Friday",
        "😘 <b>Flirty Friday</b> 😘\n"
        "All eyes on you! Today the succubi are especially playful, handing out winks, compliments, and maybe even some public flattery. Don’t be shy—flirt back for extra fun!"
    ),
    5: (
        "Sinful Saturday",
        "🔥 <b>Sinful Saturday</b> 🔥\n"
        "Indulge your wild side! Confess your fantasies, join in on spicy games, or challenge a succubus to something daring. Sinful Saturday is all about breaking the rules (but keeping it steamy and safe)!"
    ),
    6: (
        "Seduction Sunday",
        "💃 <b>Seduction Sunday</b> 💃\n"
        "The week ends with irresistible charm! The succubi will shower you with seductive greetings, tempting invites, and sweet nothings. Let yourself be drawn in—Seduction Sunday only happens once a week!"
    ),
}

DAILY_POST_HOUR = 19  # 7 PM UTC
DAILY_POST_MIN = 0

GROUPS_FILE = "data/flirty_groups.json"

def load_flirty_groups():
    import os, json
    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, "r") as f:
            return json.load(f)
    return []

def save_flirty_groups(groups):
    import json
    with open(GROUPS_FILE, "w") as f:
        json.dump(groups, f)

def register(app):
    @app.on_message(filters.command("enablethemes") & filters.group)
    async def enable_themes(client, message):
        groups = load_flirty_groups()
        if message.chat.id not in groups:
            groups.append(message.chat.id)
            save_flirty_groups(groups)
        await message.reply("✅ This group will now get daily flirty themed messages!")

    @app.on_message(filters.command("disablethemes") & filters.group)
    async def disable_themes(client, message):
        groups = load_flirty_groups()
        if message.chat.id in groups:
            groups.remove(message.chat.id)
            save_flirty_groups(groups)
        await message.reply("🚫 Daily themed messages disabled for this group.")

    @app.on_message(filters.command(["themeday", "todaystheme"]) & filters.group)
    async def today_theme(client, message):
        today = datetime.now(timezone.utc).weekday()
        name, msg = FLIRTY_THEMES[today]
        await message.reply(msg)

async def post_daily_flirty_theme(app):
    posted_today = set()
    while True:
        now = datetime.now(timezone.utc)
        if now.hour == DAILY_POST_HOUR and now.minute == DAILY_POST_MIN:
            today = now.weekday()
            name, msg = FLIRTY_THEMES[today]
            groups = load_flirty_groups()
            for chat_id in groups:
                try:
                    await app.send_message(chat_id, msg)
                except Exception as e:
                    print(f"Failed to send flirty theme to {chat_id}: {e}")
            posted_today = set(groups)
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(20)
