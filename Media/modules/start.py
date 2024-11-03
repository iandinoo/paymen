import os
import asyncio

import time
import datetime
from pytz import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta

from pyrogram import *
from pyromod import listen
from pyrogram.types import *

from . message import *
from . buttons import *

from Media.modules import atlantic
from Media.helper.tools import *

from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler

from Media import *
from Media.config import *
from Media.helper.db import *
from Media.helper.date_info import DATE, TIME

scheduler = AsyncIOScheduler()
scheduler.start()

@bot.on_message(filters.command("start") & filters.private)
@broadcast
async def start(c : Bot, cb : Message):
    maintenance = await get_maintenance()
    if maintenance == True:
        return await cb.reply_text(C20)
    try:
        welcome = await get_welcome()
        mention = f"@{cb.from_user.username}" if cb.from_user.username else cb.from_user.mention
        await cb.reply(text=welcome.format(mention=mention), reply_markup=KL10)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await cb.reply(text=welcome.format(mention=mention), reply_markup=KL10)

@bot.on_callback_query(filters.regex("withdraw"))
async def atlantic_account(c: Bot, m: CallbackQuery):
    data = await atlantic.cek_informasi_account()
         
    data = data.get('data')
    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    balance = f"Rp {int(data.get('balance', 0)):,}".replace(',', '.')
    status = data.get('status')
     
    greeting_message = ACCOUNT_ATLANTIC_MESSAGE.format(
        name=name,
        username=username,
        email=email,
        phone=phone,
        balance=balance,
        status=status,
    )
    await m.edit_message_text(greeting_message, reply_markup=KL45)

@bot.on_callback_query(filters.regex("cancel"))
async def cancel(c: Bot, cb: CallbackQuery):
     try:
          await cb.message.delete()
          await cb.answer('Canceled')
          id = await get_id(cb.from_user.id)
          p = await atlantic.cancel_deposit(id)
     except BaseException as e:
          await cb.message.reply(e)

@bot.on_callback_query(filters.regex("deposit"))
async def deposit(c: Bot, cb: CallbackQuery):
     maintenance = await get_maintenance()
     harga = await get_harga()
     if maintenance == True:
          return await cb.message.reply(C20)
     fee = 0 # otomatis dari atlantic
     nominal = int(harga) # minimal 2000
     tambahan = 0 # biaya tambahan
     metode = "qris" # metode jangan diganti
     get_balance = 0
     reff_id = await atlantic.generate_unique_ref_id()
     new_buy = await atlantic.new_deposit(
          reff_id,
          metode,
          nominal,
          tambahan,
          fee,
          get_balance,
     )
     await cb.message.delete()
     user_id = cb.from_user.id
     id = new_buy.get('data').get('id')
     await set_id(user_id, id)
     fee = new_buy.get('data').get('fee')
     fee = f"Rp. {fee:,}".replace(",", ".")
     nominal = new_buy.get('data').get('nominal')
     nominal = f"Rp. {nominal:,}".replace(",", ".")
     path = f"QRIS_{cb.id}.png"
     now = datetime.now(timezone("Asia/Jakarta"))
     expired = now + relativedelta(seconds=int(300))
     waktu = expired.strftime("%H.%M.%S")
     await atlantic.create_qris(new_buy.get('data').get('qr_string'), path)
     qris_message = await c.send_photo(
          chat_id=cb.message.chat.id, photo=path, 
          caption=C10.format(nominal=nominal,waktu=waktu,reff_id=reff_id),
          reply_markup=KL40
     )
     os.remove(path)
     start_time = int(time.time() * 1000)
     scheduler.add_job(
          func=checkPaymentStatusOrder,
          trigger=IntervalTrigger(seconds=10),
          args=(user_id, reff_id, qris_message, start_time, nominal, c, cb),
          id=f"payment_{reff_id}",
     )

async def checkPaymentStatusOrder(
     tele_uid: int,
     reff_id: str,
     qris_message,
     start_time,
     nominal,
     c: Bot,
     cb: types.CallbackQuery
):
     id = await get_id(tele_uid)
     current_time = int(time.time() * 1000)
     check = await atlantic.view_deposit(id, reff_id)
     data = check.get('data')
     links = await get_link()
     btn = link_buttons(links)
     status = data.get('status')
     user = await bot.get_users(tele_uid)
     if status == 'processing':
          await bot.send_message(
               chat_id=user.id, 
               text=C25.format(reff_id), 
               protect_content=True,
               reply_markup=btn
          )
          logger = await get_logs()
          await bot.send_message(
               chat_id=logger,
               text=C65.format(
                    user.first_name,
                    nominal,
                    reff_id[:5],
                    DATE,
                    TIME
               )
          )
          scheduler.remove_job(f"payment_{reff_id}")
     elif status == 'cancel':
          await cb.message.reply('Pembayaran dicancel!')
          await qris_message.delete()
          scheduler.remove_job(f"payment_{reff_id}")
     else:
          if current_time - start_time < 300000:
               return
          else:
               await atlantic.cancel_deposit(id)
               await cb.message.reply('❌ Qris Telah Kadaluarsa Pembayaran Dicancel, Silahkan Coba Kembali..')
               await qris_message.delete()
               scheduler.remove_job(f"payment_{reff_id}")
