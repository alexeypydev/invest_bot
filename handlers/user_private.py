from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types.callback_query import CallbackQuery

import common.text as text
from keyboards.reply import start_kb
from filters.is_investor import IsInvestor

router = Router()
router.message.filter(IsInvestor())

@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=start_kb)

@router.message(Command('help'))
async def help_handler(msg: Message):
    await msg.answer('Напиши мне @alekseypydev')


# @router.callback_query(F.data == 'orel')
# async def monetka(clbck: CallbackQuery):
#     await clbck.message.answer(text=orel(), reply_markup=kb.menu)

@router.message(Command('dice'))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji='🎲')