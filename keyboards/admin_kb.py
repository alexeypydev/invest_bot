from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start_admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Открыть временную темку')
        ],
        [
            KeyboardButton(text='Закрыть временную темку')
        ],
        [
            KeyboardButton(text='Проекты')
        ],
        [
            KeyboardButton(text='Удалить проект')
        ],
        [
            KeyboardButton(text='Добавить выплату по временной'),
            KeyboardButton(text='Добавить выплату по долгосрочной')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Управление'
)