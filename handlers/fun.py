import random
from pyrogram import filters
from handlers.xp import add_xp

TEASE_MESSAGES = [
    "{mention} gets a wicked tease. Did you feel that shiver down your spine?",
    "A sultry succubus teases {mention}—are you blushing yet?",
    "{mention} just got the kind of tease that makes your heart race.",
    "Tease delivered! {mention}, try not to melt...",
    "Who’s making {mention} squirm? Oh right, the succubi.",
    "{mention}, that was only a sample of what’s to come.",
    "Playful fingers trace up your neck, {mention}. Can you handle it?",
    "{mention}, your turn to get teased. Beg for more?",
    "A devilish whisper just for {mention}: behave... or don’t.",
    "{mention} gets the succubus treatment. We hope you like anticipation.",
]

BITE_MESSAGES = [
    "A playful bite for {mention}—did you like that?",
    "Succubi sink their teeth into {mention}. Tasty!",
    "{mention} just got marked. Welcome to the Sanctuary...",
    "A teasing nibble on your ear, {mention}. Was that too much?",
    "{mention}, you’ve been bitten! The games have only just begun.",
    "Bite delivered! {mention}, do you want another?",
    "A little love bite for {mention}. We like to leave a mark.",
    "{mention}, don’t flinch—the succubi always bite gently (at first).",
    "{mention} just got a taste of temptation.",
    "The Sanctuary claims {mention} with a spicy bite.",
]

SPANK_MESSAGES = [
    "A flirty spank for {mention}. Naughty boys get extra attention.",
    "SMACK! {mention}, the succubi know you like it.",
    "Red cheeks for {mention}—courtesy of the Sanctuary.",
    "{mention}, you’re in trouble now. Spank delivered!",
    "Who’s blushing? {mention}, behave or get another!",
    "A teasing slap for {mention}—just a warning (or is it an invitation?).",
    "Spank received! {mention}, the succubi keep score...",
    "{mention}, you asked for it. Don’t pretend you didn’t like it.",
    "A stinging reminder for {mention}. Naughty boys are our favorite.",
    "Succubus special: one spank, just for {mention}.",
]

def register(app):
    @app.on_message(filters.command("tease") & filters.group)
    async def tease(client, message):
        if not message.reply_to_message:
            await message.reply("Reply to someone to tease them!")
            return
        user = message.reply_to_message.from_user
        xp = add_xp(message.chat.id, user.id, 2)
        msg = random.choice(TEASE_MESSAGES).format(mention=user.mention)
        await message.reply(f"{msg} (+2 XP)")

    @app.on_message(filters.command("bite") & filters.group)
    async def bite(client, message):
        if not message.reply_to_message:
            await message.reply("Reply to someone to bite them!")
            return
        user = message.reply_to_message.from_user
        xp = add_xp(message.chat.id, user.id, 3)
        msg = random.choice(BITE_MESSAGES).format(mention=user.mention)
        await message.reply(f"{msg} (+3 XP)")

    @app.on_message(filters.command("spank") & filters.group)
    async def spank(client, message):
        if not message.reply_to_message:
            await message.reply("Reply to someone to spank them!")
            return
        user = message.reply_to_message.from_user
        xp = add_xp(message.chat.id, user.id, 4)
        msg = random.choice(SPANK_MESSAGES).format(mention=user.mention)
        await message.reply(f"{msg} (+4 XP)")
