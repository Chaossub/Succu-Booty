import random
from pyrogram import filters

WELCOME_MESSAGES = [
    "🔥 Welcome to Succubus Sanctuary, {mention}! Are you ready to get a little wicked tonight?",
    "💋 Look who just wandered in... {mention}, the succubi have been waiting for you.",
    "😈 Temptation just walked through the door—hi, {mention}!",
    "👠 {mention} has arrived. Let’s see how much mischief you can handle...",
    "💄 {mention}, ready to play naughty games? The succubi can’t wait to make you blush.",
    "🖤 {mention}, you’re surrounded by temptation. The real fun starts now.",
    "🔥 {mention}, step right into the den of desire. Don’t hold back...",
    "😏 The party just got hotter—{mention} is here!",
    "💦 {mention}, are you sure you can handle this much pleasure?",
    "🌶️ The succubi sense fresh energy—welcome, {mention}. Will you survive the night?",
]

GOODBYE_MESSAGES = [
    "👋 {mention} tried to escape... but the succubi always remember their favorites.",
    "💔 {mention} left the Sanctuary. We hope you’ll come back for more mischief.",
    "😏 {mention} slipped away. We were just getting started!",
    "🌙 {mention} escaped temptation (for now). The succubi are plotting your return.",
    "🖤 {mention} is gone, but their blush will linger.",
    "🔥 Another one bites the dust... or does {mention} want a second round?",
    "😈 The succubi will miss teasing you, {mention}. See you in your dreams.",
    "💋 {mention} vanished—did our flirts scare you off?",
    "🌶️ The heat just turned down a notch. Hurry back, {mention}!",
    "✨ Goodbye, {mention}. Remember: temptation is only a message away.",
]

def register(app):
    @app.on_message(filters.new_chat_members)
    async def welcome_new_member(client, message):
        for member in message.new_chat_members:
            mention = member.mention
            text = random.choice(WELCOME_MESSAGES).format(mention=mention)
            await message.reply(text)

    @app.on_message(filters.left_chat_member)
    async def goodbye_member(client, message):
        member = message.left_chat_member
        mention = member.mention
        text = random.choice(GOODBYE_MESSAGES).format(mention=mention)
        await message.reply(text)
