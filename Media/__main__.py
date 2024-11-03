import asyncio
from Media import bot
from Media.config import LOGGER
from pyrogram import idle
from Media.helper.tools import 

loop = asyncio.get_event_loop_policy().get_event_loop()

async def main():
    try:
        await bot.start()
        ex = await bot.get_me()
        user_id = ex.id
        username = ex.username
        namebot = ex.first_name
        LOGGER("INFO").info(f"{namebot} | [ @{username} ] | 🔥 BERHASIL DIAKTIFKAN! 🔥")
    except Exception as a:
        print(a)
    LOGGER("INFO").info(f"[🔥 BOT AKTIF! 🔥]")
    await idle()


LOGGER("INFO").info("Starting Bot...")
loop.run_until_complete(main())
