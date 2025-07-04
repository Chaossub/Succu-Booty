from pyrogram import filters
from handlers.utils import OWNER_ID

def register(app):
    @app.on_message(filters.command("help") & filters.group)
    async def help_cmd(client, message):
        user_id = message.from_user.id
        is_owner = (user_id == OWNER_ID)
        is_admin = False
        if not is_owner:
            try:
                member = await client.get_chat_member(message.chat.id, user_id)
                is_admin = member.status in ["administrator", "creator"]
            except Exception:
                is_admin = False
        else:
            is_admin = True

        lines = []
        lines.append("💋 <b>Succubus Sanctuary Bot Commands</b> 💋\n")

        if is_admin:
            lines.append("<b>👑 Moderation:</b>\n"
                         "/warn – Warn user (reply)\n"
                         "/flirtywarn – Flirty warn (reply)\n"
                         "/mute [time] – Mute user (reply)\n"
                         "/unmute – Unmute user (reply)\n"
                         "/kick – Kick user (reply)\n"
                         "/ban – Ban user (reply)\n"
                         "/unban – Unban user (reply)\n"
                         "/resetwarns – Reset warns (reply)\n"
                         "/warns – Check warns (reply or @user)\n")

            lines.append("<b>🌐 Federation:</b>\n"
                         "/createfed, /renamefed, /deletefed\n"
                         "/addfedadmin, /removefedadmin\n"
                         "/linkgroup, /unlinkgroup\n"
                         "/fedban, /fedunban, /fedcheck, /purgefed\n"
                         "/togglefedaction\n")

        flyer_lines = [
            "/listflyers – List flyers",
            "/flyer <name> – Show flyer"
        ]
        if is_admin:
            flyer_lines += [
                "/addflyer <name> – Add flyer (reply to image)",
                "/changeflyer <name> – Change flyer (reply to image)",
                "/deleteflyer <name> – Delete flyer",
                "/scheduleflyer <name> <YYYY-MM-DD HH:MM> – Schedule flyer"
            ]
        lines.append("<b>🎟️ Flyers:</b>\n" + "\n".join(flyer_lines) + "\n")

        lines.append(
            "<b>😈 Fun & Naughty XP:</b>\n"
            "/naughty – Your naughty meter\n"
            "/leaderboard – Top naughty users\n"
            "/tease (reply) – Tease for XP\n"
            "/spank (reply) – Spank for XP\n"
            "/bite (reply) – Bite for XP\n"
        )
        lines.append(
            "<b>📢 Summon:</b>\n"
            "/summon @user – Summon\n"
            "/flirtysummon @user – Flirty summon\n"
            "/summonall – Summon all\n"
            "/flirtysummonall – Flirty summon all\n"
            "/trackall – Track all for summon\n"
        )
        lines.append(
            "<b>🎀 Flirty Themed Days:</b>\n"
            "/themeday – Today’s flirty theme\n"
        )
        lines.append(
            "<b>💌 Other:</b>\n"
            "/cancel – Cancel a command\n"
            "/help – Show this menu"
        )

        await message.reply("\n".join(lines), parse_mode="html")
