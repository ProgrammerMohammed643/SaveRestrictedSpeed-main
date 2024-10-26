from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import time
import os
import threading

bot_token = "6749189026:AAFy2cnFDLMr_5LKPxyokd6larHh8tNWO08"  # أدخل توكن البوت هنا مباشرة
api_hash = "8dd9fb5fa2782d91b9847ace66eb885a"  # أدخل api_hash هنا
api_id = 29755247  # أدخل api_id هنا
session_string = "AgFZ12oAYv_AV16aJr_ETYMYAy__6dCzuSWdXnFY2n1u4Zp5SBckDwI01zXn1F_yQpkmJM3nwGNuUMz8QBBS78GcYGnFnC5v_Cg0a6_vXxw6Xu8eeQGwc3YzmlxTyfva9JvBBleqTbMx1y6I00q9ii-ltmHd5OsUasF4KkXUuDNhqytIj6yqhYmy7wbY0vqkCPkiVay7GXgm2RvMjtGroTzxknta5Sv7kyfiaU-VYF4uGmCPH1hhr0e3YA_EGIUwqKGAEN1xtADYpYarEYZxRCGc_ub76u31toQWnFbbtjt7Qm-Gi_MJQqAKlaek7EC_1UXh4T2Cs2q43twHbxR_s7D8DpzOMAAAAAGzpydNAA"  # أدخل الجلسة الخاصة بك هنا

bot = Client("mybot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# إعداد الجلسة باستخدام session_string المحددة
acc = Client("myacc", api_id=api_id, api_hash=api_hash, session_string=session_string)

# بدء الجلسة
acc.start()

USAGE = """**FOR PUBLIC CHATS**

**__just send post/s link__**

**FOR PRIVATE CHATS**

**__first send invite link of the chat (unnecessary if the account of string session already member of the chat) then send post/s link__**


**MULTI POSTS**

**__send public/private posts link as explained above with format "from - to" to send multiple messages like below__**
```
https://t.me/xxxx/1001-1010

https://t.me/c/xxxx/101 - 120
```
**__note that space in between doesn't matter__**
"""
# download status
def downstatus(statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break

    time.sleep(3)
    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            bot.edit_message_text(message.chat.id, message.id, f"__Downloaded__ : **{txt}**")
            time.sleep(10)
        except:
            time.sleep(5)

# upload status
def upstatus(statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break

    time.sleep(3)
    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            bot.edit_message_text(message.chat.id, message.id, f"__Uploaded__ : **{txt}**")
            time.sleep(10)
        except:
            time.sleep(5)

# progress writer
def progress(current, total, message, type):
    with open(f'{message.id}{type}status.txt', "w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")

# start command
@bot.on_message(filters.command(["start"]))
async def send_start(client: Client, message):
    await bot.send_message(
        message.chat.id,
        f"**👋 Hi {message.from_user.mention}, I am Save Restricted Bot, I can send you restricted content by its post link**\n\n{USAGE}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⁽ ᔆᴾᴱᴱᴰ ™ ⌁ ₎ 🧃", url="t.me/JJ7AA")]])
    )

# handle incoming messages
@bot.on_message(filters.text)
async def save(client: Client, message):
    print(message.text)

    # joining chats
    if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:
        if acc is None:
            await bot.send_message(message.chat.id, f"**String Session is not Set**")
            return

        try:
            try:
                await acc.join_chat(message.text)
            except Exception as e:
                await bot.send_message(message.chat.id, f"**Error** : __{e}__")
                return
            await bot.send_message(message.chat.id, "**Chat Joined**")
        except UserAlreadyParticipant:
            await bot.send_message(message.chat.id, "**Chat already Joined**")
        except InviteHashExpired:
            await bot.send_message(message.chat.id, "**Invalid Link**")

    # getting message
    elif "https://t.me/" in message.text:
        datas = message.text.split("/")
        temp = datas[-1].replace("?single", "").split("-")
        fromID = int(temp[0].strip())
        try:
            toID = int(temp[1].strip())
        except:
            toID = fromID

        for msgid in range(fromID, toID + 1):
            # private
            if "https://t.me/c/" in message.text:
                chatid = int("-100" + datas[4])

                if acc is None:
                    await bot.send_message(message.chat.id, f"**String Session is not Set**")
                    return

                await handle_private(message, chatid, msgid)

            # bot
            elif "https://t.me/b/" in message.text:
                username = datas[4]

                if acc is None:
                    await bot.send_message(message.chat.id, f"**String Session is not Set**")
                    return
                try:
                    await handle_private(message, username, msgid)
                except Exception as e:
                    await bot.send_message(message.chat.id, f"**Error** : __{e}__")

            # public
            else:
                username = datas[3]

                try:
                    msg = await bot.get_messages(username, msgid)
                except UsernameNotOccupied:
                    await bot.send_message(message.chat.id, f"**The username is not occupied by anyone**")
                    return

                try:
                    await bot.copy_message(message.chat.id, msg.chat.id, msg.id)
                except:
                    if acc is None:
                        await bot.send_message(message.chat.id, f"**String Session is not Set**")
                        return
                    try:
                        await handle_private(message, username, msgid)
                    except Exception as e:
                        await bot.send_message(message.chat.id, f"**Error** : __{e}__")

            # wait time
            time.sleep(3)

# handle private messages
async def handle_private(message, chatid, msgid):
    msg = await acc.get_messages(chatid, msgid)
    msg_type = get_message_type(msg)

    if "Text" == msg_type:
        await bot.send_message(message.chat.id, msg.text, entities=msg.entities)
        return

    smsg = await bot.send_message(message.chat.id, '__Downloading__')
    dosta = threading.Thread(target=lambda: downstatus(f'{message.id}downstatus.txt', smsg), daemon=True)
    dosta.start()
    file = await acc.download_media(msg, progress=progress, progress_args=[message, "down"])
    os.remove(f'{message.id}downstatus.txt')

    upsta = threading.Thread(target=lambda: upstatus(f'{message.id}upstatus.txt', smsg), daemon=True)
    upsta.start()

    if "Document" == msg_type:
        try:
            thumb = await acc.download_media(msg.document.thumbs[0].file_id)
        except:
            thumb = None

        await bot.send_document(message.chat.id, file, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, progress=progress, progress_args=[message, "up"])
        if thumb is not None:
            os.remove(thumb)

    elif "Video" == msg_type:
        try:
            thumb = await acc.download_media(msg.video.thumbs[0].file_id)
        except:
            thumb = None

        await bot.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, progress=progress, progress_args=[message, "up"])
        if thumb is not None:
            os.remove(thumb)

    elif "Animation" == msg_type:
        await bot.send_animation(message.chat.id, file)

    elif "Sticker" == msg_type:
        await bot.send_sticker(message.chat.id, file)

    elif "Voice" == msg_type:
        await bot.send_voice(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, progress=progress, progress_args=[message, "up"])

    elif "Audio" == msg_type:
        try:
            thumb = await acc.download_media(msg.audio.thumbs[0].file_id)
        except:
            thumb = None

        await bot.send_audio(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, progress=progress, progress_args=[message, "up"])
        if thumb is not None:
            os.remove(thumb)

    elif "Photo" == msg_type:
        await bot.send_photo(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities)

    os.remove(file)
    if os.path.exists(f'{message.id}upstatus.txt'):
        os.remove(f'{message.id}upstatus.txt')
    await bot.delete_messages(message.chat.id, [smsg.id])

# get the type of message
def get_message_type(msg):
    try:
        msg.document.file_id
        return "Document"
    except:
        pass

    try:
        msg.video.file_id
        return "Video"
    except:
        pass

    try:
        msg.animation.file_id
        return "Animation"
    except:
        pass

    try:
        msg.sticker.file_id
        return "Sticker"
    except:
        pass

    try:
        msg.voice.file_id
        return "Voice"
    except:
        pass

    try:
        msg.audio.file_id
        return "Audio"
    except:
        pass

    try:
        msg.photo.file_id
        return "Photo"
    except:
        pass

    try:
        msg.text
        return "Text"
    except:
        pass

# infinity polling
bot.run()
