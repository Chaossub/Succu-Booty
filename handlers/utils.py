OWNER_ID = 6964994611

def admin_only(func):
    async def wrapper(client, message):
        # Owner override
        if message.from_user and message.from_user.id == OWNER_ID:
            return await func(client, message)
        try:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status not in ["administrator", "creator"]:
                return await message.reply("Admins only!")
            return await func(client, message)
        except Exception:
            return await message.reply("Admins only!")
    return wrapper
