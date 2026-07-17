import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from config import BOT_TOKEN
from states import Form
from handlers import (
    cmd_start, back_to_main, show_booking, back_to_booking,
    universal_booking, process_format, process_day_selection,
    process_time_selection, process_name, process_phone
)


bot = Bot(token = BOT_TOKEN)
dp = Dispatcher()

# reg handlers

@dp.message(CommandStart())
async def start_handler(message: Message):
    await cmd_start(message)


@dp.callback_query(F.data == "back_to_main")
async def back_main_handler(callback: CallbackQuery):
    await back_to_main(callback)


@dp.callback_query(F.data == "book_online")
async def booking_handler(callback: CallbackQuery):
    await show_booking(callback)


@dp.callback_query(F.data == "back_to_booking")
async def back_booking_handler(callback: CallbackQuery):
    await back_to_booking(callback)


@dp.callback_query(F.data.startswith("book:"))
async def booking_type_handler(callback: CallbackQuery, state):
    await universal_booking(callback, state)


@dp.callback_query(F.data.startswith("format:"))
async def format_handler(callback: CallbackQuery, state):
    await process_format(callback, state)


@dp.callback_query(F.data.startswith("day:"))
async def day_handler(callback: CallbackQuery, state):
    await process_day_selection(callback, state)


@dp.callback_query(F.data.startswith("time:"))
async def time_handler(callback: CallbackQuery, state):
    await process_time_selection(callback, state)


@dp.message(Form.name)
async def name_handler(message: Message, state):
    await process_name(message, state)


@dp.message(Form.phone)
async def phone_handler(message: Message, state):
    await process_phone(message, state)


# start bot

async def main():
    print("Бот запущений...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())