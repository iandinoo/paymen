import os
import asyncio

from pyrogram import *
from pyromod import listen
from pyrogram.types import *

from . message import *
from . buttons import *

from Media.modules import atlantic
from Media.helper.tools import *

from Media import *
from Media.config import *
from Media.helper.db import *

@bot.on_callback_query(filters.regex("wd"))
async def wd(c: Bot, cb: CallbackQuery):
    await cb.answer(C120, cache_time=0, show_alert=True)

@bot.on_callback_query(filters.regex("Kosong"))
async def kosong(c: Bot, cb: CallbackQuery):
    await cb.answer(C115, cache_time=0, show_alert=True)
    
@bot.on_callback_query(filters.regex("AKI1"))
async def list_harga_1(c: Bot, m: CallbackQuery):
    code = "DANA1"
    data = await atlantic.list_harga(code)
    data = data.get('data')
    harga =  f"Rp {int(data.get('price')):,}".replace(',', '.')
    try:
        status = data.get('status')
        if status == 'available':
            status = 'Tersedia'
        elif status == 'empty':
            status = 'Kosong'
        else:
            pass
        await set_code(
            m.from_user.id, 
            code
        )
        note = data.get('note')
        layanan = data.get('name')
        prov = data.get('provider')
        gori = data.get('category')
        await set_price(
            m.from_user.id,
            data.get('price'),
        )
        btn = withdraw_btn(status)
        await m.edit_message_text(
            text=C105.format(
                layanan,prov,
                gori,
                status,harga,
                note
            ), 
            reply_markup=btn
        )
    except BaseException as e:
        await m.edit_message_text(e)

@bot.on_callback_query(filters.regex("AKI2"))
async def list_harga_2(c: Bot, m: CallbackQuery):
    code = "DANA10"
    data = await atlantic.list_harga(code)
    data = data.get('data')
    harga =  f"Rp {int(data.get('price')):,}".replace(',', '.')
    try:
        status = data.get('status')
        if status == 'available':
            status = 'Tersedia'
        elif status == 'empty':
            status = 'Kosong'
        else:
            pass
        await set_code(
            m.from_user.id, 
            code
        )
        note = data.get('note')
        layanan = data.get('name')
        prov = data.get('provider')
        gori = data.get('category')
        await set_price(
            m.from_user.id,
            data.get('price'),
        )
        btn = withdraw_btn(status)
        await m.edit_message_text(
            text=C105.format(
                layanan,prov,
                gori,
                status,harga,
                note
            ), 
            reply_markup=btn
        )
    except BaseException as e:
        await m.edit_message_text(e)
        
@bot.on_callback_query(filters.regex("AKI3"))
async def list_harga_3(c: Bot, m: CallbackQuery):
    code = "DANA20"
    data = await atlantic.list_harga(code)
    data = data.get('data')
    harga =  f"Rp {int(data.get('price')):,}".replace(',', '.')
    try:
        status = data.get('status')
        if status == 'available':
            status = 'Tersedia'
        elif status == 'empty':
            status = 'Kosong'
        else:
            pass
        await set_code(
            m.from_user.id, 
            code
        )
        note = data.get('note')
        layanan = data.get('name')
        prov = data.get('provider')
        gori = data.get('category')
        await set_price(
            m.from_user.id,
            data.get('price'),
        )
        btn = withdraw_btn(status)
        await m.edit_message_text(
            text=C105.format(
                layanan,prov,
                gori,
                status,harga,
                note
            ), 
            reply_markup=btn
        )
    except BaseException as e:
        await m.edit_message_text(e)

@bot.on_callback_query(filters.regex("AKI4"))
async def list_harga_4(c: Bot, m: CallbackQuery):
    code = "DANA50"
    data = await atlantic.list_harga(code)
    data = data.get('data')
    harga =  f"Rp {int(data.get('price')):,}".replace(',', '.')
    try:
        status = data.get('status')
        if status == 'available':
            status = 'Tersedia'
        elif status == 'empty':
            status = 'Kosong'
        else:
            pass
        await set_code(
            m.from_user.id, 
            code
        )
        note = data.get('note')
        layanan = data.get('name')
        prov = data.get('provider')
        gori = data.get('category')
        await set_price(
            m.from_user.id,
            data.get('price'),
        )
        btn = withdraw_btn(status)
        await m.edit_message_text(
            text=C105.format(
                layanan,prov,
                gori,
                status,harga,
                note
            ), 
            reply_markup=btn
        )
    except BaseException as e:
        await m.edit_message_text(e)
        
