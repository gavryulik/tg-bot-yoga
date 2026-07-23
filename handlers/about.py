from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from keyboards import get_main_menu

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
    
async def back_to_main(callback: CallbackQuery):
    await callback.message.answer(
        text="Привіт! 👋\nЯ — помічник Валентини. Оберіть послугу:",
        reply_markup=get_main_menu()
    )

    await callback.message.delete()
    
    await callback.answer()