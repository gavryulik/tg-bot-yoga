from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🛒 Купити курс", callback_data="buy_course"))
    builder.row(InlineKeyboardButton(text="📅 Записатися онлайн", callback_data="book_online"))
    builder.row(InlineKeyboardButton(text="👤 Про мене", callback_data="about_me"))
    return builder.as_markup()

def get_booking_menu():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🧘‍♀️ Ха-тха йога", callback_data="book:hatha"))
    builder.row(InlineKeyboardButton(text="🤰 Йога для вагітних", callback_data="book:pregnant"))
    builder.row(InlineKeyboardButton(text="✨ Sound Healing", callback_data="book:sound"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))
    return builder.as_markup()

def get_format_menu():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="👤 Індивідуальне", callback_data="format:individual"))
    builder.row(InlineKeyboardButton(text="👥 Групове", callback_data="format:group"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_booking"))
    return builder.as_markup()

def get_courses_menu():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🤰 Йога для вагітних", callback_data="course:pregnant", style="primary"))
    builder.row(InlineKeyboardButton(text="🦴 Йога для здорового хребта", callback_data="course:spine", style="primary"))
    builder.row(InlineKeyboardButton(text="✨ Жіноча гормональна йога", callback_data="course:hormonal", style="primary"))
    builder.row(InlineKeyboardButton(text="🔵 Чакральна йога", callback_data="course:chakra", style="primary"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))
    return builder.as_markup()