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
                "Great! Now send a description for your federation, or /cancel to abort."
            )
            return

        if step == 2:
            set_session_data(message.chat.id, message.from_user.id, "desc", message.text.strip())
            data = session["data"]
            fed_id = str(message.chat.id)
            fed_doc = {
                "_id": fed_id,
                "owner": message.from_user.id,
                "admins": [],
                "groups": [message.chat.id],
                "bans": [],
                "name": data["name"],
                "desc": data["desc"],
                "action": "kick",
            }
            feds.insert_one(fed_doc)
            await message.reply(
                f"✅ Federation '{data['name']}' created!\nDescription: {data['desc']}"
            )
            end_session(message.chat.id, message.from_user.id)
            return

    @app.on_message(filters.command("cancel") & filters.group)
    async def cancel_cmd(client, message):
        if get_session(message.chat.id, message.from_user.id):
            end_session(message.chat.id, message.from_user.id)
            await message.reply("Operation canceled.")
        else:
            await message.reply("No operation to cancel.")

    @app.on_message(filters.command("renamefed") & filters.group)
    @admin_only
    async def rename_fed(client, message):
        fed = get_fed_by_group(message.chat.id)
        if not fed or not is_fed_admin(message.from_user.id, fed):
            await message.reply("You are not an admin of the federation.")
            return
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply("Usage: /renamefed <new_name>")
            return
        feds.update_one({"_id": fed["_id"]}, {"$set": {"name": args[1]}})
        await message.reply("✅ Federation renamed!")

    @app.on_message(filters.command("deletefed") & filters.group)
    @admin_only
    async def delete_fed(client, message):
        fed = get_fed_by_group(message.chat.id)
        if not fed or not is_fed_admin(message.from_user.id, fed):
            await message.reply("You are not an admin of the federation.")
            return
        feds.delete_one({"_id": fed["_id"]})
        await message.reply("❌ Federation deleted and unlinked from all groups.")

    @app.on_message(filters.command("addfedadmin") & filters.group)
    @admin_only
    async def add_fed_admin(client, message):
        fed = get_fed_by_group(message.chat.id)
        if not fed or message.from_user.id != fed["owner"]:
            await message.reply("Only the federation owner can add admins.")
            return
        if not message.reply_to_message:
            await message.reply("Reply to a user to add as federation admin.")
            return
        user_id = message.reply_to_message.from_user.id
        if user_id in fed.get("admins", []):
            await message.reply("User is already a federation admin.")
            return
        feds.update_one({"_id": fed["_id"]}, {"$push": {"admins": user_id}})
        await message.reply("✅ User added as federation admin.")

    @app.on_message(filters.command("removefedadmin") & filters.group)
    @admin_only
    async def remove_fed_admin(client, message):
        fed = get_fed_by_group(message.chat.id)
        if not fed or message.from_user.id != fed["owner"]:
            await message.reply("Only the federation owner can remove admins.")
            return
        if not message.reply_to_message:
            await message.reply("Reply to a user to remove as federation admin.")
            return
        user_id = message.reply_to_message.from_user.id
        if user_id not in fed.get("admins", []):
            await message.reply("User is not a federation admin.")
            return
        feds.update_one({"_id": fed["_id"]}, {"$pull": {"admins": user_id}})
        await message.reply("✅ User removed from federation admins.")

    @app.on_message(filters.command("linkgroup") & filters.group)
    @admin_only
    async def link_group(client, message):
        fed = get_fed_by_group(message.chat.id)
        if not fed or not is_fed_admin(message.from_user.id, fed):
            await message.reply("You are not an admin of the federation.")
            return
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply("Usage: /linkgroup <chat_id>")
            return
        try:
            group_id = int(args[1])
        except ValueError:
            await message.reply("Invalid chat ID.")
            return
        if group_id in fed.get("groups", []):
            await message.reply("Group already linked.")
            return
        feds.update_one({"_id": fed["_id"]}, {"$push": {"groups": group_id}})
        await message.reply("✅ Group linked to federation.")

    @app.on_message(filters.command("unlinkgroup") & filters.group)
    @admin_only
    async def unlink_group(client, message):
        fed = get_fed_by_group(message.chat.id)
        if not fed or not is_fed_admin(message.from_user.id, fed):
            await message.reply("You are not an admin of the federation.")
            return
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply("Usage: /unlinkgroup <chat_id>")
            return
        try:
            group_id = int(args[1])
        except ValueError:
            await message.reply("Invalid chat ID.")
            return
        if group_id not in fed.get("groups", []):
            await message.reply("Group not linked.")
            return
        feds.update_one({"_id": fed["_id"]}, {"$pull": {"groups": group_id}})
        await message.reply("✅ Group unlinked from federation.")

    @app.on_message(filters.command("fedban") & filters.group)
    @admin_only
    async def fed_ban(client, message):
        fed = get_fed_by_group(message.chat.id)
        if not fed or not is_fed_admin(message.from_user.id, fed):
            await message.reply("You are not an admin of the federation.")
            return
        if not message.reply_to_message:
            await message.reply("Reply to a user to fedban.")
            return
        user_id = message.reply_to_message.from_user.id
        if user_id in fed.get("bans", []):
            await message.reply("User already federationally banned.")
            return
        feds.update_one({"_id": fed["_id"]}, {"$push": {"bans": user_id}})
        await message.reply(f"User {user_id} has been federationally banned.")

    @app.on_message(filters.command("fedunban") & filters.group)
    @admin_only
    async def fed_unban(client, message):
        fed = get_fed_by_group(message.chat.id)
        if not fed or not is_fed_admin(message.from_user.id, fed):
            await message.reply("You are not an admin of the federation.")
            return
        if not message.reply_to_message:
            await message.reply("Reply to a user to fedunban.")
            return
        user_id = message.reply_to_message.from_user.id
        if user_id not in fed.get("bans", []):
            await message.reply("User is not federationally banned.")
            return
        feds.update_one({"_id": fed["_id"]}, {"$pull": {"bans": user_id}})
        await message.reply(f"User {user_id} has been federationally unbanned.")

    @app.on_message(filters.command("fedcheck") & filters.group)
    async def fed_check(client, message):
        fed = get_fed_by_group(message.chat.id)
        if not fed:
            await message.reply("No federation found for this group.")
            return
        if not message.reply_to_message:
            await message.reply("Reply to a user to check fedban status.")
            return
        user_id = message.reply_to_message.from_user.id
        if user_id in fed.get("bans", []):
            await message.reply("This user is federationally banned.")
        else:
            await message.reply("This user is not federationally banned.")

    @app.on_message(filters.command("purgefed") & filters.group)
    @admin_only
    async def purge_fed(client, message):
        fed = get_fed_by_group(message.chat.id)
        if not fed or message.from_user.id != fed["owner"]:
            await message.reply("Only the federation owner can purge bans and groups.")
            return
        feds.update_one(
            {"_id": fed["_id"]}, {"$set": {"bans": [], "groups": [message.chat.id]}}
        )
        await message.reply(
            "Federation ban list and group links purged (except this group)."
        )

    @app.on_message(filters.command("togglefedaction") & filters.group)
    @admin_only
    async def toggle_fed_action(client, message):
        fed = get_fed_by_group(message.chat.id)
        if not fed or not is_fed_admin(message.from_user.id, fed):
            await message.reply("You are not an admin of the federation.")
            return
        action = fed.get("action", "kick")
        actions = ["kick", "mute", "off"]
        idx = (actions.index(action) + 1) % len(actions)
        new_action = actions[idx]
        feds.update_one({"_id": fed["_id"]}, {"$set": {"action": new_action}})
        await message.reply(f"Federation ban action set to: {new_action.upper()}")

    @app.on_message(filters.new_chat_members)
    async def enforce_fedban_on_join(client, message):
        fed = get_fed_by_group(message.chat.id)
        if not fed or fed.get("action", "kick") == "off":
            return
        for member in message.new_chat_members:
            if member.id in fed.get("bans", []):
                try:
                    if fed["action"] == "kick":
                        await client.kick_chat_member(message.chat.id, member.id)
                        await message.reply(
                            f"User {member.mention} is federationally banned and was kicked."
                        )
                    elif fed["action"] == "mute":
                        await client.restrict_chat_member(message.chat.id, member.id, permissions=None)
                        await message.reply(
                            f"User {member.mention} is federationally banned and was muted."
                        )
                except Exception as e:
                    await message.reply(
                        f"Failed to enforce fedban for {member.mention}: {e}"
                    )

