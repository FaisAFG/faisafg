"""Default Permission in Telegram 5.0.1
Available Commands: .lock <option>, .unlock <option>, .locks
API Options: msg, media, sticker, gif, gamee, ainline, gpoll, adduser, cpin, changeinfo
DB Options: bots, commands, email, forward, url"""

from telethon import events, functions, types
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="lock( (?P<target>\S+)|$)"))
async def _(event):
     # Space weirdness in regex required because argument is optional and other
     # commands start with ".lock"
    if event.fwd_from:
        return
    input_str = event.pattern_match.group("target")
    peer_id = event.chat_id
    if input_str in (("ربات", "دستور", "ایمیل", "اشتراک", "لینک")):
        try:
            from sql_helpers.locks_sql import update_lock
        except Exception as e:
            logger.info("DB_URI is not configured.")
            logger.info(str(e))
            return False
        update_lock(peer_id, input_str, True)
        await event.edit(
            "قفل شد {}".format(input_str)
        )
    else:
        msg = None
        media = None
        sticker = None
        gif = None
        gamee = None
        ainline = None
        gpoll = None
        adduser = None
        cpin = None
        changeinfo = None
        if input_str:
            if "پیام" in input_str:
                msg = True
            if "فایل" in input_str:
                media = True
            if "استیکر" in input_str:
                sticker = True
            if "گیف" in input_str:
                gif = True
            if "بازی" in input_str:
                gamee = True
            if "خطی" in input_str:
                ainline = True
            if "نظرسنجی" in input_str:
                gpoll = True
            if "اضافه کاربر" in input_str:
                adduser = True
            if "پین" in input_str:
                cpin = True
            if "تغییر اطلاعات" in input_str:
                changeinfo = True
        banned_rights = types.ChatBannedRights(
            until_date=None,
            # view_messages=None,
            send_messages=msg,
            send_media=media,
            send_stickers=sticker,
            send_gifs=gif,
            send_games=gamee,
            send_inline=ainline,
            send_polls=gpoll,
            invite_users=adduser,
            pin_messages=cpin,
            change_info=changeinfo,
        )
        try:
            result = await event.client(
                functions.messages.EditChatDefaultBannedRightsRequest(
                    peer=peer_id,
                    banned_rights=banned_rights
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
        else:
            await event.edit(
                "قفل با موفقیت فعال شد"
            )


@borg.on(admin_cmd(pattern="unlock ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    try:
        from sql_helpers.locks_sql import update_lock
    except Exception as e:
        logger.info("DB_URI is not configured.")
        logger.info(str(e))
        return False
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    if input_str in (("ربات", "دستور", "ایمیل", "اشتراک", "لینک")):
        update_lock(peer_id, input_str, False)
        await event.edit(
            "UnLocked {}".format(input_str)
        )
    else:
        await event.edit(
            " `.lock` را بنویسید بدون هیچ دامنه ای"
        )


@borg.on(admin_cmd(pattern="curenabledlocks"))
async def _(event):
    if event.fwd_from:
        return
    try:
        from sql_helpers.locks_sql import get_locks
    except Exception as e:
        logger.info("DB_URI is not configured.")
        logger.info(str(e))
        return False
    res = ""
    current_db_locks = get_locks(event.chat_id)
    if not current_db_locks:
        res = "*قفل های گروه*"
    else:
        res = "موارد قفل شده 👇: \n"
        res += "👉 `ربات`: `{}`\n".format(current_db_locks.bots)
        res += "👉 `دستور`: `{}`\n".format(current_db_locks.commands)
        res += "👉 `ایمیل`: `{}`\n".format(current_db_locks.email)
        res += "👉 `اشتراک`: `{}`\n".format(current_db_locks.forward)
        res += "👉 `لینک`: `{}`\n".format(current_db_locks.url)
    current_chat = await event.get_chat()
    try:
        current_api_locks = current_chat.default_banned_rights
    except AttributeError as e:
        logger.info(str(e))
    else:
        res += "\nموارد قفل شده 👇: \n"
        res += "👉 `پیام`: `{}`\n".format(current_api_locks.send_messages)
        res += "👉 `فایل`: `{}`\n".format(current_api_locks.send_media)
        res += "👉 `اشتیکر`: `{}`\n".format(current_api_locks.send_stickers)
        res += "👉 `گیف`: `{}`\n".format(current_api_locks.send_gifs)
        res += "👉 `بازی`: `{}`\n".format(current_api_locks.send_games)
        res += "👉 `خطی`: `{}`\n".format(current_api_locks.send_inline)
        res += "👉 `نظرسنجی`: `{}`\n".format(current_api_locks.send_polls)
        res += "👉 `اضافه کاربر`: `{}`\n".format(current_api_locks.invite_users)
        res += "👉 `پین`: `{}`\n".format(current_api_locks.pin_messages)
        res += "👉 `تغییر اطلاعات`: `{}`\n".format(current_api_locks.change_info)
    await event.edit(res)


@borg.on(events.MessageEdited())  # pylint:disable=E0602
@borg.on(events.NewMessage())  # pylint:disable=E0602
async def check_incoming_messages(event):
    try:
        from sql_helpers.locks_sql import update_lock, is_locked
    except Exception as e:
        logger.info("DB_URI is not configured.")
        logger.info(str(e))
        return False
    # TODO: exempt admins from locks
    peer_id = event.chat_id
    if is_locked(peer_id, "دستور"):
        entities = event.message.entities
        is_command = False
        if entities:
            for entity in entities:
                if isinstance(entity, types.MessageEntityBotCommand):
                    is_command = True
        if is_command:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "من به مقام آدمین دسترسی ندارم. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "دستور", False)
    if is_locked(peer_id, "اشتراک"):
        if event.fwd_from:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "من به مقام آدمین دسترسی ندارم. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "اشترک", False)
    if is_locked(peer_id, "ایمیل"):
        entities = event.message.entities
        is_email = False
        if entities:
            for entity in entities:
                if isinstance(entity, types.MessageEntityEmail):
                    is_email = True
        if is_email:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "من به مقام آدمین دسترسی . \n`{}`".format(str(e))
                )
                update_lock(peer_id, "ایمیل", False)
    if is_locked(peer_id, "لینک"):
        entities = event.message.entities
        is_url = False
        if entities:
            for entity in entities:
                if isinstance(entity, (types.MessageEntityTextUrl, types.MessageEntityUrl)):
                    is_url = True
        if is_url:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(
                    "من به مقام آدمین دسترسی ندارم. \n`{}`".format(str(e))
                )
                update_lock(peer_id, "url", False)


@borg.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    try:
        from sql_helpers.locks_sql import update_lock, is_locked
    except Exception as e:
        logger.info("DB_URI is not configured.")
        logger.info(str(e))
        return False
    # TODO: exempt admins from locks
    # check for "lock" "bots"
    if is_locked(event.chat_id, "ربات"):
        # bots are limited Telegram accounts,
        # and cannot join by themselves
        if event.user_added:
            users_added_by = event.action_message.from_id
            is_ban_able = False
            rights = types.ChatBannedRights(
                until_date=None,
                view_messages=True
            )
            added_users = event.action_message.action.users
            for user_id in added_users:
                user_obj = await event.client.get_entity(user_id)
                if user_obj.bot:
                    is_ban_able = True
                    try:
                        await event.client(functions.channels.EditBannedRequest(
                            event.chat_id,
                            user_obj,
                            rights
                        ))
                    except Exception as e:
                        await event.reply(
                            "من به مقام آدمین دسترسی ندارم. \n`{}`".format(str(e))
                        )
                        update_lock(event.chat_id, "bots", False)
                        break
            if Config.G_BAN_LOGGER_GROUP is not None and is_ban_able:
                ban_reason_msg = await event.reply(
                    "!warn [user](tg://user?id={}) لطفا در این گروه ربات اضافه نکنید.".format(users_added_by)
                )
