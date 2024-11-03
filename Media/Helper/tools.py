import asyncio

from Media.helper.db import *
from pytz import timezone
from pyrogram import *
from pyrogram.types import *

import datetime
from datetime import datetime
from typing import Union, List
from Media.modules import atlantic

async def get_readable_time(seconds: int) -> str:    
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time
    
def get_arg(message: Message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])
  
def broadcast(func):
    async def wrapper(client, message):
        user_id = str(message.from_user.id)
        broadcast = await get_gcast()
        if user_id not in broadcast:
            await add_gcast(user_id)
        await func(client, message)
    return wrapper

def balance(func):
    async def wrapper(client, m):
        data = await atlantic.cek_informasi_account()
        balance = data.get('data').get('balance')
        price = await get_price(m.from_user.id)
        if balance < price:
            return await m.answer(C110, cache_time=0, show_alert=True)
        await func(client, m)
    return wrapper
