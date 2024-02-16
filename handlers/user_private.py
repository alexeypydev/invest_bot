from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command, or_f
from aiogram.types.callback_query import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from common.text import greet, shortprojects_greet
from database.orm_query import orm_get_projects, orm_add_user, orm_get_projects_available
from keyboards.reply import start_kb, shortprojects_kb
from filters.is_investor import IsInvestor

router = Router()
router.message.filter(IsInvestor())

@router.message(Command('start'))
async def start_handler(msg: Message, session: AsyncSession):
    await msg.answer_sticker(sticker='CAACAgIAAxkBAAELZ6dlzdKIR-0_ivZrbXE_jivVdFOasgACfQMAAm2wQgO9Ey75tk26UzQE')
    await msg.answer(greet.format(name=msg.from_user.full_name), reply_markup=start_kb)
    await orm_add_user(session, msg.from_user)


@router.message(Command('menu'))
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
            await msg.answer(f'<i>{project.name}</i>\n\n⚜️Инвест: {project.cost}\n⚜️Доход: {project.profit}\n⚜️Гарантия: {project.guarantee}\n⚜️Результат: {project.result_date.strftime("%d.%m.%y")}\n⚜️Срок ответа: {project.deadline_date.strftime("%d.%m.%y %H:%M")}\n⚜️Мест: {project.place}')
    else:
        await msg.answer('Доступных проектов нет 😿')