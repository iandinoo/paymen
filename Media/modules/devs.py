import time 
import asyncio 

import datetime
from pyrogram import *
from pyrogram.types import *

from . message import *
from . buttons import *

from Media import *
from Media.helper.db import *
from Media.helper.tools import *

StartTime = time.time()

@bot.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(c : Bot, cb : Message):
    try:
        links = await get_link()
        logger = await get_logs()
        gucast = await get_gcast()
        end = datetime.now()
        start = datetime.now()
        forcesub = await get_forcesub()
        duration = (end - start).microseconds / 1000
        uptime = await get_readable_time((time.time() - StartTime))
        await cb.reply(
            text=C60
            .format(
                len(gucast),
                duration,
                uptime,
                forcesub,
                logger,
                links
            ),
            reply_markup=KL20
        )
    except BaseException as e:
        await cb.reply(f'{e}')
        return

@bot.on_callback_query(filters.regex("HG0"))	
async def HG0(client: Bot, cb: CallbackQuery):
    try:
        links = await get_link()
        logger = await get_logs()
        gucast = await get_gcast()
        end = datetime.now()
        start = datetime.now()
        forcesub = await get_forcesub()
        duration = (end - start).microseconds / 1000
        uptime = await get_readable_time((time.time() - StartTime))
        await cb.edit_message_text(
            text=C60
            .format(
                len(gucast),
                duration,
                uptime,
                forcesub,
                logger,
                links
            ),
            reply_markup=KL20
        )
    except BaseException as e:
        await cb.edit_message_text(f'{e}')
        return

@bot.on_callback_query(filters.regex("HG1"))	
async def HG1(client: Bot, cb: CallbackQuery):
    try:
        await cb.edit_message_text(text=C80, reply_markup=KL35)
    except BaseException as e:
        await cb.edit_message_text(f"{e}")
        return 
        pass
        
@bot.on_callback_query(filters.regex("HG2"))	
async def HG2(client: Bot, cb: CallbackQuery):
    try:
        maintenance = await get_maintenance()
        if maintenance == True:
            maintenance = "✅"
        elif maintenance == False:
            maintenance = "❌"
        else:
            pass
        broadcast = await get_type()
        if broadcast == True:
            broadcast = "Copy"
        elif broadcast == False:
            broadcast = "Forward"
        else:
            pass
        await cb.edit_message_text(text=C70.format(maintenance,broadcast), reply_markup=KL25)
    except BaseException as e:
        await cb.edit_message_text(f"{e}")
        return 
        pass

@bot.on_callback_query(filters.regex("HG3"))	
async def HG3(client: Bot, cb: CallbackQuery):
    try:
        await maintenance_on(cb)
        await cb.edit_message_text(text=C75, reply_markup=KL30)
    except BaseException as e:
        await cb.edit_message_text(f"{e}")
        return 
        pass

@bot.on_callback_query(filters.regex("HG4"))	
async def HG4(client: Bot, cb: CallbackQuery):
    try:
        await maintenance_off(cb)
        await cb.edit_message_text(text=C75, reply_markup=KL30)
    except BaseException as e:
        await cb.edit_message_text(f"{e}")
        return 
        pass

@bot.on_callback_query(filters.regex("HG5"))	
async def HG5(client: Bot, cb: CallbackQuery):
    try:
        await type_on(cb)
        await cb.edit_message_text(text=C75, reply_markup=KL30)
    except BaseException as e:
        await cb.edit_message_text(f"{e}")
        return 
        pass

@bot.on_callback_query(filters.regex("HG6"))	
async def HG6(client: Bot, cb: CallbackQuery):
    try:
        await type_off(cb)
        await cb.edit_message_text(text=C75, reply_markup=KL30)
    except BaseException as e:
        await cb.edit_message_text(f"{e}")
        return 
        pass

@bot.on_callback_query(filters.regex("close"))	
async def HG6(client: Bot, cb: CallbackQuery):
    await cb.message.delete()
    
@bot.on_message(filters.command("set_harga") & filters.private & filters.user(OWNER_ID))
async def setharga(c:Bot, cb :Message):
    msg = get_arg(cb)

    if not msg:
        return await cb.reply("❌ Gunakan Format /set_harga (jumlah)")

    try:
        await set_harga(int(msg))
        xx = await cb.reply_text(C40)
        await asyncio.sleep(10)
        await xx.delete()
    except BaseException as e:
        cx = await cb.reply_text(f"{e}")
        await asyncio.sleep(10)
        await cx.delete()
        return
        pass

@bot.on_message(filters.command("set_forcesub") & filters.private & filters.user(OWNER_ID))
async def setforcesub(c : Bot, message : Message):
    text = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        text = message.text.split()
        if len(text) < 2:
            await message.reply_text("❌ Format Salah..!\nGunakan Format `/set_forcesub [username]` tanpa @ dan https")
            await message.delete()
            return
        username = text[1]
        try:
            db = await bot.get_chat(username)
            await set_forcesub(db.username)
            await message.reply(C55)
            await asyncio.sleep(10)
            await message.delete()
        except BaseException as e:
            cx = await message.reply_text(f"❌ Username Tidak Ditemukan.")
            await asyncio.sleep(10)
            await cx.delete()
            return
            pass
        
@bot.on_message(filters.command("set_logs") & filters.private & filters.user(OWNER_ID))
async def setlogs(c : Bot, message : Message):
    text = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        text = message.text.split()
        if len(text) < 2:
            await message.reply_text("❌ Format Salah..!\nGunakan Format `/set_logs [username]`")
            await message.delete()
            return
        username = text[1]
        try:
            db = await bot.get_chat(username)
            await set_logs(db.username)
            await message.reply(C85)
            await asyncio.sleep(10)
            await message.delete()
        except BaseException as e:
            cx = await message.reply_text(f"❌ Username Tidak Ditemukan.")
            await asyncio.sleep(10)
            await cx.delete()
            return
            pass
            
@bot.on_message(filters.command("set_link") & filters.private & filters.user(OWNER_ID))
async def setlinks(c:Bot, cb :Message):
    msg = get_arg(cb)

    if not msg:
        xc = await cb.reply(text="❌ Gunakan Format /set_link (link) (link harus berupa https atau t.me)")
        await asyncio.sleep(10)
        await xc.delete()
        return
        
    try:
        await set_link(msg)
        oo = await cb.reply_text(C30)
        await asyncio.sleep(10)
        await oo.delete()
    except BaseException as e:
        return await cb.reply_text(f"{e}")
        
@bot.on_message(filters.command("set_welcome") & filters.private & filters.user(OWNER_ID))
async def setwelcome(c:Bot, cb :Message):
    msg = get_arg(cb)

    if not msg:
        await cb.reply(text="❌ Gunakan Format /set_link (link) (link harus berupa https atau t.me)")
        return
        
    try:
        await set_welcome(msg)
        await cb.reply_text(C35)
    except BaseException as e:
        return await cb.reply_text(f"{e}")

async def send_msg(chat_id, message: Message):
    try:
        broadcast = await get_type()
        if broadcast == False:
            await message.forward(chat_id=chat_id)
        elif broadcast == True:
            await message.copy(chat_id=chat_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(int(e.value))
        return send_msg(chat_id, message)
        
@bot.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client : Bot, message : Message):
    users = await get_gcast()
    msg = get_arg(message)
    if message.reply_to_message:
        msg = message.reply_to_message

    if not msg:
        await message.reply(text="**Reply atau berikan saya sebuah pesan!**")
        return
    
    out = await message.reply(text="**Memulai Broadcast...**")
    
    if not users:
        await out.edit(text="**Maaf, Broadcast Gagal Karena Belum Ada user**")
        return
    
    done = 0
    failed = 0
    for user in users:
        try:
            await send_msg(user, message=msg)
            done += 1
        except:
            failed += 1
    await out.edit(f"✅ **Berhasil Mengirim Pesan Ke {done} User.**\n❌ **Gagal Mengirim Pesan Ke {failed} User.**")
    
