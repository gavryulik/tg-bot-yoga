import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext


from config import BOT_TOKEN
from states import Form
from handlers import (
    cmd_start, back_to_main, show_booking, back_to_booking,
    universal_booking, process_format, process_day_selection,
    process_time_selection, process_name, process_phone, show_courses, show_course_detail, show_about_me, deep_link_start, buy_course, receipt_handler, approve_payment, reject_payment
)


bot = Bot(token = BOT_TOKEN)
dp = Dispatcher()

# reg handlers

@dp.message(CommandStart())
async def start_handler(
    message: Message,
    command: CommandObject,
    state: FSMContext,
):
    await deep_link_start(message, command, state)


@dp.callback_query(F.data == "back_to_main")
async def back_main_handler(callback: CallbackQuery):
    await back_to_main(callback)


@dp.callback_query(F.data == "book_online")
async def booking_handler(callback: CallbackQuery):
    await show_booking(callback)


@dp.callback_query(F.data == "back_to_booking")
async def back_booking_handler(callback: CallbackQuery):
    await back_to_booking(callback)
    
@dp.callback_query(F.data == "about_me")
async def about_me_handler(callback: CallbackQuery):
    await show_about_me(callback)


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
    
@dp.callback_query(F.data == "buy_course")
async def buy_course_handler(callback: CallbackQuery):
    await show_courses(callback)

@dp.callback_query(F.data.startswith("course:"))
async def course_detail_handler(callback: CallbackQuery):
    await show_course_detail(callback)
    
@dp.callback_query(F.data.startswith("buy:"))
async def buy_course_handler(callback: CallbackQuery, state: FSMContext):
    await buy_course(callback, state)
    
@dp.message(Form.receipt, F.photo)
async def receipt_photo_handler(message: Message, state: FSMContext):
    await receipt_handler(message, state)
    
@dp.message(Form.receipt, F.document)
async def receipt_document_handler(message: Message, state: FSMContext):
    await receipt_handler(message, state)
    
@dp.callback_query(F.data.startswith("approve:"))
async def approve_handler(callback: CallbackQuery):
    await approve_payment(callback)

@dp.callback_query(F.data.startswith("reject:"))
async def reject_handler(callback: CallbackQuery):
    await reject_payment(callback) 

#@dp.message(F.photo)
#async def get_photo_file_id(message: Message):
    # message.photo[-1]
    #photo_id = message.photo[-1].file_id
    
    #print(f"\n[FILE ID]: {photo_id}\n")
    
    #await message.reply(f"Реплика вашего file_id:\n<code>{photo_id}</code>", parse_mode="HTML")


# start bot

async def main():
    print("Бот запущений...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())