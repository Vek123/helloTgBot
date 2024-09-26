import asyncio
from datetime import datetime

import httpx
from aiogram import Bot, Router, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from motor import motor_asyncio

from settings import config
from structures.UserStruct import User


cluster = motor_asyncio.AsyncIOMotorClient(config.MONGODB_CLUSTER_URL)
collection = cluster.User_DB.users
default_router = Router()

START_MESSAGE = "Добрый день. Как вас зовут?"


class UserInfo(StatesGroup):
    name = State()


async def addUser(user_id: int, name: str):
    date = str(datetime.now())
    user = User(user_id, name, date)
    existing_user = await collection.find_one(user_id)
    if existing_user:
        await collection.replace_one(existing_user, user.__dict__)
        return
    await collection.insert_one(user.__dict__)


@default_router.message(CommandStart())
async def bot_start(message: Message, state: FSMContext):
    await state.set_state(UserInfo.name)
    await message.answer(START_MESSAGE)


@default_router.message(UserInfo.name)
async def confirm_name(message: Message, state: FSMContext):
    await addUser(message.chat.id, message.text)
    await state.clear()
    client = httpx.AsyncClient()
    vault = await client.get(config.CURRENCY_API_URL)
    await client.aclose()

    await message.answer(
        "Рад знакомству, %(name)s! Курс доллара сегодня %(vault)sр"
        % {
            "name": message.text,
            "vault": str(round(vault.json()["data"]["RUB"]["value"], 2)),
        }
    )


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(default_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
