from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types.callback_query import CallbackQuery

import text
import kb
from utils import orel

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)

@router.message(Command("help"))
async def help_handler(msg: Message):
    await msg.answer("Напиши мне @alekseypydev")


@router.callback_query(F.data == "orel")
async def monetka(clbck: CallbackQuery):
    await clbck.message.answer(text=orel(), reply_markup=kb.menu)

@router.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")