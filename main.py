import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode #содержит настройки разметки сообщений (HTML, Markdown)
from aiogram.fsm.storage.memory import MemoryStorage # хранилища данных для состояний пользователей

from handlers.handlers import router
from common.bot_cmds_list import private

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

TOKEN = os.getenv('TOKEN', 'Here must be token!')

async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML) # отвечает за используемую по умолчанию разметку сообщений. Мы используем HTML, чтобы избежать проблем с экранированием символов.
    dp = Dispatcher(storage=MemoryStorage()) # все данные бота, которые мы не сохраняем в БД (к примеру состояния), будут стёрты при перезапуске. Этот вариант является оптимальным, так как хранение состояний диспетчера требуется редко.
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats()) # удаляет все обновления, которые произошли после последнего завершения работы бота.
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()) # второй параметр зачем?


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())