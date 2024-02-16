from datetime import datetime
from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_add_poject, orm_delete_project, orm_get_project, orm_get_projects, orm_update_poject

from filters.is_admin import IsAdmin
from keyboards.admin_kb import start_admin_kb
from keyboards.inline import get_callback_btns


admin_router = Router()
admin_router.message.filter(IsAdmin())

@admin_router.message(Command('admin'))
async def start_admin_handler(msg: types.Message):
    await msg.answer(text='Что сделать?', reply_markup=start_admin_kb)

@admin_router.message(F.text == 'Проекты')
async def starring_at_project(msg: types.Message, session: AsyncSession):
    for project in await orm_get_projects(session):
        await msg.answer(
            text=f'{project.name}',
            reply_markup=get_callback_btns(btns={
                'Удалить': f'delete_{project.id}',
                'Изменить': f'change_{project.id}'
            })
        )
    await msg.answer('Ок, вот список темок')


@admin_router.callback_query(F.data.startswith('delete_'))
async def delete_project(callback: types.CallbackQuery, session: AsyncSession):
    project_id = callback.data.split('_')[-1]
    await orm_delete_project(session, int(project_id))
    await callback.answer('Проект удален', show_alert=True)
    await callback.message.answer('Проект удален!')


@admin_router.message(F.text == 'Удалить проект')
async def starring_at_project(msg: types.Message, session: AsyncSession):
    project_id = 1
    await orm_delete_project(session, project_id)
    await msg.answer('Удалил')

class AddProject(StatesGroup):
    name = State()
    cost = State()
    profit = State()
    guarantee = State()
    result_date = State()
    deadline_date = State()
    place = State()

    project_for_change = None

@admin_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_project_callback(
    callback: types.CallbackQuery, state: FSMContext, session: AsyncSession
):
    project_id = callback.data.split("_")[-1]

    project_for_change = await orm_get_project(session, int(project_id))

    AddProject.project_for_change = project_for_change

    await callback.answer()
    await callback.message.answer(
        'Название темки', reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProject.name)


@admin_router.message(StateFilter(None), F.text == 'Открыть временную темку')
async def add_temka(msg: types.Message, state: FSMContext):
    await msg.answer(text='Название темки', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddProject.name)

@admin_router.message(StateFilter('*'), Command("отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return
    if AddProject.project_for_change:
        AddProject.project_for_change = None
    await state.clear()
    await message.answer("Действия отменены", reply_markup=start_admin_kb)

@admin_router.message(AddProject.name, F.text)
async def add_name(msg: types.Message, state: FSMContext):
    if msg.text == '.':
        await state.update_data(name=AddProject.project_for_change.name)
    else:
        await state.update_data(name=msg.text)
    await msg.answer(text='Сумма захода')
    await state.set_state(AddProject.cost)

@admin_router.message(AddProject.cost, F.text)
async def add_cost(msg: types.Message, state: FSMContext):
    if msg.text == '.':
        await state.update_data(cost=AddProject.project_for_change.cost)
    else:
        await state.update_data(cost=msg.text)
    await msg.answer(text='Доход')
    await state.set_state(AddProject.profit)

@admin_router.message(AddProject.profit, F.text)
async def add_profit(msg: types.Message, state: FSMContext):
    if msg.text == '.':
        await state.update_data(profit=AddProject.project_for_change.profit)
    else:
        await state.update_data(profit=msg.text)
    await msg.answer(text='Гарантии')
    await state.set_state(AddProject.guarantee)

@admin_router.message(AddProject.guarantee, F.text)
async def add_guarantee(msg: types.Message, state: FSMContext):
    if msg.text == '.':
        await state.update_data(guarantee=AddProject.project_for_change.guarantee)
    else:
        await state.update_data(guarantee=msg.text)
    await msg.answer(text='Дата результата\nФормат: 01.01.2000')
    await state.set_state(AddProject.result_date)

@admin_router.message(AddProject.result_date, F.text)
async def add_result(msg: types.Message, state: FSMContext):
    if msg.text == '.':
        await state.update_data(result_date=AddProject.project_for_change.result_date)
    else:
        await state.update_data(result_date=datetime.strptime(msg.text, '%d.%m.%Y').date())
    await msg.answer(text='Дедлайн ответа\nФормат: 01.01.2000 00:00')
    await state.set_state(AddProject.deadline_date)

@admin_router.message(AddProject.deadline_date, F.text)
async def add_deadline(msg: types.Message, state: FSMContext):
    if msg.text == '.':
        await state.update_data(deadline_date=AddProject.project_for_change.deadline_date)
    else:
        await state.update_data(deadline_date=datetime.strptime(msg.text, '%d.%m.%Y %H:%M'))
    await msg.answer(text='Количество мест')
    await state.set_state(AddProject.place)

@admin_router.message(AddProject.place, F.text)
async def add_place(msg: types.Message, state: FSMContext, session: AsyncSession):
    if msg.text == '.':
        await state.update_data(place=AddProject.project_for_change.place)
    else:
        await state.update_data(place=msg.text)
    data = await state.get_data()
    try:
        if AddProject.project_for_change:
            await orm_update_poject(session, AddProject.project_for_change.id, data)
            await msg.answer(text='Темка изменена', reply_markup=start_admin_kb)
        else:
            await orm_add_poject(session, data)
            await msg.answer(text='Темка добавлена', reply_markup=start_admin_kb)
        await state.clear()
    except Exception as error:
        await msg.answer(f'Что-то пошло не так: {error}', reply_markup=start_admin_kb)
        await state.clear()
    
    AddProject.project_for_change = None