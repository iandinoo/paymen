from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from Media.helper.db import *
from pyrogram.types import *
from pyrogram import *
from Media import *
import asyncio

def force_channel(forcesub, username):
    FORCESUB = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(f"Bergabung Ke Channel", url=f"t.me/{forcesub}"),
            ],
            [
                InlineKeyboardButton(f"Coba Lagi", url=f"http://t.me/{username}?start=start"),
            ]
        ]
    )
    return FORCESUB
    
@bot.on_message(filters.incoming & filters.private, group=-1)
async def ForceSub(app: Bot, message: Message):
    forcesub = await get_forcesub()
    if not forcesub:  # Not compulsory
        return
    try:
        try:
            c = await bot.get_me()
            await app.get_chat_member(forcesub, message.from_user.id)
        except UserNotParticipant:
            if forcesub.isalpha():
                link = "https://t.me/" + forcesub
            else:
                chat_info = await app.get_chat(forcesub)
                link = chat_info.invite_link
            try:
                username = c.username
                btn = force_channel(
                    forcesub,
                    username
                )
                await message.reply(
                    f"<b>{message.from_user.first_name}</b> Belum bergabung dichannel kami, silahkan bergabung lalu coba lagi.",
                    disable_web_page_preview=True,
                    reply_markup=btn)

                await message.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        await message.reply_text(C50.format(forcesub))
