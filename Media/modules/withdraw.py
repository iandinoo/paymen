import os
import time
import asyncio

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

scheduler = AsyncIOScheduler()
scheduler.start()
     
@bot.on_callback_query(filters.regex("Tersedia"))
@balance
async def tersedia(c: Bot, cb: CallbackQuery):
    user_id = cb.from_user.id
    while True:
        try:  
            data = await cb.edit_message_text(f'<b>🤖 Bot:</b> Masukan Nomor Tujuan Menggunakan 08:')
        except:
            data = cb.message
        
        result = await c.listen(cb.from_user.id, (filters.user(cb.from_user.id)))
        if not result.text:
            await result.delete()
            continue
        try:
            target = result.text
            if len(result.text) < 10:
                p = await result.reply('<b>🤖 Bot:</b> Nomer Harus Minimal 10 digit..!')
                await asyncio.sleep(3)
                await result.delete()
                await p.delete()
                continue
        except:
            p = await result.reply('<b>🤖 Bot:</b> Pastikan angka bukan huruf..!')
            await asyncio.sleep(3)
            await result.delete()
            await p.delete()
            continue
        break
    await cb.message.delete()
    user_id = cb.from_user.id
    code = await get_code(user_id)
    reff_id = await atlantic.generate_unique_ref_id()
    new_buy = await atlantic.new_transaksi(
         reff_id,code,target,
    )
    trx = new_buy.get('data').get('id')
    await set_id(cb.from_user.id, trx)
    price = new_buy.get('data').get('price')
    nominal = f"Rp {int(new_buy.get('data').get('price')):,}".replace(',', '.')
    pending_msg = await cb.message.reply(
         text=C90.format(
              trx,reff_id,nominal,
         )
    )
    start_time = int(time.time() * 1000)
    scheduler.add_job(
         func=checkPaymentStatusOrder,
         trigger=IntervalTrigger(seconds=10),
         args=(user_id, reff_id, pending_msg, start_time, nominal, c, cb),
         id=f"payment_{reff_id}",
    )
     
               
async def checkPaymentStatusOrder(
     user_id: int,
     reff_id: str,
     pending_msg,
     start_time,
     nominal,
     c: Bot,
     cb: types.CallbackQuery
):
     id = await get_id(user_id)
     check = await atlantic.status_transaksi(
          id, reff_id
     )
     data = check.get('data')
     status = data.get('status')
     if status == 'success':
          await cb.message.reply(
               text=C95.format(
                    id, reff_id,
                    nominal
               )
          )
          await pending_msg.delete()
          scheduler.remove_job(f"payment_{reff_id}")
     elif status == 'failed':
          await cb.message.reply(
               text=C100.format(
                    id,reff_id,
                    nominal
               )
          )
          await pending_msg.delete()
          scheduler.remove_job(f"payment_{reff_id}")
     else:
          pass
