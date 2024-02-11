from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Краткосрочные инвестиции')
        ],
        [
            KeyboardButton(text='Долгосрочные инвестиции')
        ],
        [
            KeyboardButton(text='Мой профиль'),
            KeyboardButton(text='О проекте')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='С чего начнем?'
)
