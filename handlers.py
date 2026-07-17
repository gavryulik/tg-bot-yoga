from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from states import Form
from keyboards import get_main_menu, get_booking_menu, get_format_menu
from sheets import get_available_days, get_available_times, save_to_gsheet

# HANDLERS

async def cmd_start(message: Message):
    await message.answer_video_note(
        video_note="DQACAgIAAxkBAAMLalevFd4EZrLKB6eh8B6zB0CnyxMAAjOcAAINGrhKJ8MGvTU7htw9BA"
    )
    await message.answer(
        "Привіт! 👋\nЯ — помічник Валентини. Оберіть послугу:",
        reply_markup=get_main_menu()
    )


async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "Привіт! 👋\nЯ — помічник Валентини. Оберіть послугу:",
        reply_markup=get_main_menu()
    )


async def show_booking(callback: CallbackQuery):
    await callback.message.edit_text(
        "Оберіть практику:",
        reply_markup=get_booking_menu()
    )


async def back_to_booking(callback: CallbackQuery):
    await callback.message.edit_text(
        "Оберіть практику:",
        reply_markup=get_booking_menu()
    )


async def universal_booking(callback: CallbackQuery, state: FSMContext):
    services = {
        "hatha": "Ха-тха йога",
        "pregnant": "Йога для вагітних",
        "sound": "Sound Healing"
    }
    code = callback.data.split(":")[1]
    service_name = services.get(code)
    
    await state.update_data(chosen_yoga=service_name)

    if code == "sound":
        await state.set_state(Form.name)
        await callback.message.edit_text("Дякую! Як до вас звертатися? (Введіть ім'я)")
    else:
        await state.set_state(Form.format)
        await callback.message.edit_text("Оберіть формат:", reply_markup=get_format_menu())


async def process_format(callback: CallbackQuery, state: FSMContext):
    format_type = "Індивідуальне" if callback.data.split(":")[1] == "individual" else "Групове"
    await state.update_data(format=format_type)

    data = await state.get_data()
    days = get_available_days(data['chosen_yoga'], format_type)

    builder = InlineKeyboardBuilder()
    for day in days:
        builder.row(InlineKeyboardButton(text=day, callback_data=f"day:{day}"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_booking"))

    await callback.message.edit_text("Оберіть день:", reply_markup=builder.as_markup())


async def process_day_selection(callback: CallbackQuery, state: FSMContext):
    day = callback.data.split(":")[1]
    await state.update_data(day=day)
    data = await state.get_data()

    times = get_available_times(data['chosen_yoga'], data['format'], day)

    builder = InlineKeyboardBuilder()
    for time in times:
        builder.row(InlineKeyboardButton(text=time, callback_data=f"time:{time}"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_booking"))

    await callback.message.edit_text(f"Вільний час на {day}:", reply_markup=builder.as_markup())


async def process_time_selection(callback: CallbackQuery, state: FSMContext):
    time = callback.data.split(":")[1]
    await state.update_data(time=time)
    await state.set_state(Form.name)
    await callback.message.edit_text("Дякую! Як до вас звертатися? (Введіть ім'я)")


async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()

    if data.get('chosen_yoga') == "Sound Healing":
        await state.set_state(Form.phone)
        await message.answer("Дякую! Тепер введіть номер телефону з '+' (напр. +380...):")
    else:
        await state.set_state(Form.phone)
        await message.answer("Дякую! Тепер введіть номер телефону з '+' (напр. +380...):")


async def process_phone(message: Message, state: FSMContext):
    if not message.text.startswith("+") or not message.text[1:].isdigit():
        return await message.answer("Помилка! Введіть номер з плюсом.")

    await state.update_data(phone=message.text)
    data = await state.get_data()

    save_to_gsheet(data)

    chosen_yoga = data.get('chosen_yoga', 'Невідомо')
    
    if chosen_yoga == "Sound Healing":
        summary = (f"🔔 **Нова заявка!**\n\n"
                   f"✨ Послуга: Sound Healing\n"
                   f"👤 Ім'я: {data['name']}\n"
                   f"📱 Тел: {data['phone']}")
    else:
        summary = (f"🔔 **Нова заявка!**\n\n"
                   f"🧘‍♀️ Послуга: {chosen_yoga}\n"
                   f"👤 Формат: {data.get('format', '—')}\n"
                   f"👤 Ім'я: {data['name']}\n"
                   f"📱 Тел: {data['phone']}\n"
                   f"📅 День: {data.get('day', '—')}\n"
                   f"⏰ Час: {data.get('time', '—')}")

    for admin_id in [929571161, 931723030]:
        try:
            await message.bot.send_message(chat_id=admin_id, text=summary)
        except:
            pass

    await message.answer("Дякую! Заявку надіслано. Валентина скоро зв'яжеться з вами!")
    await state.clear()