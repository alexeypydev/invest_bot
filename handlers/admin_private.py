from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from filters.is_admin import IsAdmin
from keyboards.admin_kb import start_admin_kb


admin_router = Router()
admin_router.message.filter(IsAdmin())

@admin_router.message(Command('admin'))
async def start_admin_handler(msg: types.Message):
    await msg.answer(text='Что сделать?', reply_markup=start_admin_kb)

class AddProject(StatesGroup):
    name = State()
    invest = State()
    dohod = State()
    garantiya = State()
    result_date = State()
    deadline = State()
    mest = State()

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

    await state.clear()
    await message.answer("Действия отменены", reply_markup=start_admin_kb)

@admin_router.message(AddProject.name, F.text)
async def add_name(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer(text='Сумма захода')
    await state.set_state(AddProject.invest)

@admin_router.message(AddProject.invest, F.text)
async def add_invest(msg: types.Message, state: FSMContext):
    await state.update_data(invest=msg.text)
    await msg.answer(text='Доход')
    await state.set_state(AddProject.dohod)

@admin_router.message(AddProject.dohod, F.text)
async def add_dohod(msg: types.Message, state: FSMContext):
    await state.update_data(dohod=msg.text)
    await msg.answer(text='Гарантии')
    await state.set_state(AddProject.garantiya)

@admin_router.message(AddProject.garantiya, F.text)
async def add_garantii(msg: types.Message, state: FSMContext):
    await state.update_data(garantiya=msg.text)
    await msg.answer(text='Дата результата')
    await state.set_state(AddProject.result_date)

@admin_router.message(AddProject.result_date, F.text)
async def add_result(msg: types.Message, state: FSMContext):
    await state.update_data(result_date=msg.text)
    await msg.answer(text='Дедлайн ответа')
    await state.set_state(AddProject.deadline)

@admin_router.message(AddProject.deadline, F.text)
async def add_deadline(msg: types.Message, state: FSMContext):
    await state.update_data(deadline=msg.text)
    await msg.answer(text='Количество мест')
    await state.set_state(AddProject.mest)

@admin_router.message(AddProject.mest, F.text)
async def add_mest(msg: types.Message, state: FSMContext):
    await state.update_data(mest=msg.text)
    await msg.answer(text='Темка добавлена', reply_markup=start_admin_kb)
    data = await state.get_data()
    await msg.answer(text=str(data))
    await state.clear()