from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandObject

from states import Form
from keyboards import get_main_menu, get_booking_menu, get_format_menu, get_courses_menu
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
    await callback.message.answer(
        text="Привіт! 👋\nЯ — помічник Валентини. Оберіть послугу:",
        reply_markup=get_main_menu()
    )

    await callback.message.delete()
    
    await callback.answer()


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
    
async def show_about_me(callback: CallbackQuery):
    about_text = (
        "Вітаю! Я Валентина, професійний інструктор з йоги. "
        "Тут ви можете слідкувати за моїм життям та корисними порадами:"
    )

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📱 Instagram", url="https://www.instagram.com/gavryul1ik?igsh=d2xreTlqbnlpdTlj"))
    builder.row(InlineKeyboardButton(text="🎵 TikTok", url="https://www.tiktok.com/@jcdshbvfcgj?_r=1&_t=ZS-989lIbQEM4n"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))
    
    await callback.message.delete()
    await callback.message.answer(about_text, reply_markup=builder.as_markup())
    await callback.answer()
    
async def show_courses(callback: CallbackQuery):
    photo_file_id = "AgACAgIAAxkBAAIC9WpbzkWN3Zf9kpca4tJ7qdvZ6SnyAAK9Gmsb4KvhSmV1GyaIbTyvAQADAgADeQADPQQ"
    
    text = ("Вітаю! 🙏 Я рада, що ви тут.\n\n"
            "Мене звати Валентина, я професійний викладач йоги з багаторічним досвідом. Моя мета — зробити практику йоги доступною, безпечною та по-справжньому ефективною для кожного, незалежно від рівня підготовки."
            "Я створила ці авторські курси, щоб допомогти вам налагодити контакт із власним тілом, відновити енергію та покращити здоров'я, не виходячи з дому. Кожна програма — це поєднання перевірених технік, моєї підтримки та вашого бажання стати кращою версією себе.\n\n"
            "Оберіть програму, яка відгукується вашому стану сьогодні:")
    
    await callback.message.delete()
    
    await callback.message.answer_photo(
        photo=photo_file_id,
        caption=text,
        parse_mode="Markdown",
        reply_markup=get_courses_menu()
    )

async def send_course(message: Message, code: str):

    if code == "pregnant":
        photo_id = "AgACAgIAAxkBAAIDmGpdN18ZiwWQGO__INDUGsGBCEs6AAI6I2sb4KvpSgJSv4jVMkssAQADAgADeQADPQQ"

        short_text = (
            "🤰 **Йога для вагітних**\n\n"
            "М’яка підтримка вашого тіла та розуму в цей особливий період. "
            "Програма допомагає зняти напругу в спині, підготувати тіло до пологів "
            "та наповнитися спокоєм."
        )

        detail_text = (
            "**Йога для вагітних** (12 занять + бонус)\n\n"
            "12 днів дбайливої турботи про себе та малюка.\n\n"
            "○ Що всередині:\n\n"
            "• 12 відео-уроків\n"
            "• Бонус: Гайд «Як розслабитися за 5 хвилин»\n"
            "• Доступ відкривається автоматично щодня\n"
            "• Результат: легкість у спині та спокійний сон."
        )

    elif code == "spine":

        photo_id = "AgACAgIAAxkBAAIDmmpdN3N_Jyexv_jY-KwGKkSsglKwAAI9I2sb4KvpSu94XXaeMfH5AQADAgADeQADPQQ"

        short_text = (
            "🦴 **Йога для здорового хребта**\n\n"
            "Ваш хребет — це опора всього організму."
        )

        detail_text = (
            "**Йога для здорового хребта** (14 занять + бонус)\n\n"
            "2 тижні інтенсивної роботи над поставою.\n\n"
            "○ Що всередині:\n\n"
            "• 14 комплексів\n"
            "• Бонус\n"
            "• Новий урок щодня\n"
            "• Результат: здорова спина."
        )

    elif code == "hormonal":

        photo_id = "AgACAgIAAxkBAAIDnGpdN5BdwuyjOFUkzcaIGLI7kFGlAAI_I2sb4KvpStefVAcX09dnAQADAgADeQADPQQ"

        short_text = (
            "✨ **Жіноча гормональна йога**\n\n"
            "Практика для жіночого здоров'я."
        )

        detail_text = (
            "**Жіноча гормональна йога** (12 занять + бонус)\n\n"
            "12 практик для відновлення гормонального балансу."
        )

    elif code == "chakra":

        photo_id = "AgACAgIAAxkBAAIDnmpdN6YbdUFu25wx7J2zgr4NAh_IAAJAI2sb4KvpSjbDDVOllYXjAQADAgADeQADPQQ"

        short_text = (
            "🔵 **Чакральна йога**\n\n"
            "7 практик для гармонізації енергії."
        )

        detail_text = (
            "**Чакральна йога** (7 занять + бонус)\n\n"
            "Практика роботи з усіма чакрами."
        )

    else:
        await message.answer("Курс не знайдено.")
        return

    await message.answer_photo(
        photo=photo_id,
        caption=short_text,
        parse_mode="Markdown",
    )

    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="💰 Купити курс",
            callback_data=f"buy:{code}",
        )
    )

    builder.row(
        InlineKeyboardButton(
            text="🔙 Назад до курсів",
            callback_data="buy_course",
        )
    )

    await message.answer(
        detail_text,
        parse_mode="Markdown",
        reply_markup=builder.as_markup(),
    )

async def show_course_detail(callback: CallbackQuery):
    code = callback.data.split(":")[1]

    await send_course(callback.message, code)

    await callback.answer()


async def deep_link_start(
    message: Message,
    command: CommandObject,
    state: FSMContext,
):
    if command.args:

        code = command.args

        if code.startswith("course_"):

            code = code.replace("course_", "")

            if code in (
                "pregnant",
                "spine",
                "hormonal",
                "chakra",
            ):
                await send_course(message, code)
                return

    await cmd_start(message)