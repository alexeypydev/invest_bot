from aiogram import F, Router, types
from aiogram.filters import Command, or_f
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from common.text import greet, shortprojects_greet
from database.orm_query import (
    orm_add_user,
    orm_get_projects_available,
)
from filters.is_investor import IsInvestor
from keyboards.inline import get_callback_btns
from keyboards.reply import shortprojects_kb, start_kb

router = Router()
router.message.filter(IsInvestor())

@router.message(Command('start'))
async def start_handler(msg: Message, session: AsyncSession):
    await msg.answer_sticker(sticker='CAACAgIAAxkBAAELZ6dlzdKIR-0_ivZrbXE_jivVdFOasgACfQMAAm2wQgO9Ey75tk26UzQE')
    await msg.answer(greet.format(name=msg.from_user.full_name), reply_markup=start_kb)
    await orm_add_user(session, msg.from_user)


@router.message(or_f(Command('menu'), F.text == 'Назад'))
async def menu_handler(msg: Message):
    await msg.answer('Главное меню:', reply_markup=start_kb)


@router.message(Command('help'))
async def help_handler(msg: Message):
    await msg.answer('Напиши мне @alekseypydev')

    
@router.message(F.text == 'Краткосрочные инвестиции')
async def shortprojects_handler(msg: types.Message):
    await msg.answer(shortprojects_greet, reply_markup=shortprojects_kb)


@router.message(F.text == 'Доступные')
async def shortprojects_available_handler(msg: types.Message, session: AsyncSession):
    results = await orm_get_projects_available(session)
    if results:
        for project in results:
            await msg.answer(
                f'<i>{project.name}</i>\n\n⚜️Инвест: {project.cost}\n'
                f'⚜️Доход: {project.profit}\n⚜️Гарантия: {project.guarantee}\n'
                f'⚜️Результат: {project.result_date.strftime("%d.%m.%y")}\n'
                f'⚜️Срок ответа: {project.deadline_date.strftime("%d.%m.%y %H:%M")}\n'
                f'⚜️Мест: {project.place}',
                reply_markup=get_callback_btns(btns={
                    'Участвовать': f'take_{project.id}'
                })
            )
    else:
        await msg.answer('Доступных проектов нет 😿')

@router.callback_query(F.data.startswith('take_'))
async def take_project(callback: types.CallbackQuery):
    project_id = callback.data.split('_')[-1]
    await callback.message.answer(
        f'Дальше будет FSM с данными с проектом {project_id}',
        reply_markup=types.ReplyKeyboardRemove()
    )
