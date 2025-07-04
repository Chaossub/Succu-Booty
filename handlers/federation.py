from pyrogram import filters
from handlers.utils import admin_only

def register(app):
    @app.on_message(filters.command("createfed") & filters.group)
    @admin_only
    async def create_fed(client, message):
        await message.reply("✅ Federation created! (Federation logic to be expanded)")

    @app.on_message(filters.command("fedban") & filters.group)
    @admin_only
    async def fed_ban(client, message):
        await message.reply("✅ Federation ban issued! (Federation logic to be expanded)")

