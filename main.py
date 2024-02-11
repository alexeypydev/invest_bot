import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.user_private import router
from handlers.admin_private import admin_router
from common.bot_cmds_list import private

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

TOKEN = os.getenv('TOKEN', 'Here must be token!')
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
bot.my_admins_list = [280220020]
bot.my_allowed_users = [280220020, 501713966, 454921615, 877962787, 6391248030]

dp = Dispatcher()
dp.include_routers(router, admin_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())