from aiogram.filters import Filter
from aiogram import Bot, types

class IsInvestor(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        return message.from_user.id in bot.my_allowed_users