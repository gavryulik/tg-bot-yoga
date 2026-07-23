from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from states import Form

async def buy_course(callback: CallbackQuery, state: FSMContext):
    code = callback.data.split(":")[1]

    await state.update_data(course=code)
    await state.set_state(Form.receipt)

    text = (
        "💳 **Оплата курсу**\n\n"
        "Для отримання доступу до курсу здійсніть оплату.\n\n"
        "🏦 **IBAN:**\n"
        "`UAxxxxxxxxxxxxxxxxxxxxxxxx`\n\n"
        "👤 Отримувач:\n"
        "Валентина ...\n\n"
        "💰 Сума:\n"
        "799 грн\n\n"
        "Після оплати просто надішліть сюди фото або PDF квитанції."
    )

    await callback.message.answer(
        text,
        parse_mode="Markdown"
    )

    await callback.answer()
    
async def receipt_handler(message: Message, state: FSMContext):

    data = await state.get_data()

    course_names = {
        "pregnant": "Йога для вагітних",
        "spine": "Йога для здорового хребта",
        "hormonal": "Жіноча гормональна йога",
        "chakra": "Чакральна йога",
    }

    course = course_names.get(data.get("course"), "Невідомий курс")

    caption = (
        "💳 **Нова оплата курсу**\n\n"
        f"📚 Курс: {course}\n"
        f"👤 {message.from_user.full_name}\n"
        f"🆔 {message.from_user.id}"
    )
    
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="✅ Підтвердити",
            callback_data=f"approve:{message.from_user.id}"
        ),
        InlineKeyboardButton(
            text="❌ Відхилити",
            callback_data=f"reject:{message.from_user.id}"
        )
    )

    for admin_id in [929571161, 931723030]:
        try:
            if message.photo:
                await message.bot.send_photo(
                    admin_id,
                    photo=message.photo[-1].file_id,
                    caption=caption,
                    parse_mode="Markdown",
                    reply_markup=builder.as_markup()
                )

            elif message.document:
                await message.bot.send_document(
                    admin_id,
                    document=message.document.file_id,
                    caption=caption,
                    parse_mode="Markdown",
                    reply_markup=builder.as_markup()
                )

        except Exception as e:
            print(e)

    await message.answer(
        "✅ Дякуємо!\n\n"
        "Ми отримали вашу квитанцію.\n"
        "Після перевірки оплати відкриємо вам доступ до курсу."
    )

    await state.clear()
    
async def approve_payment(callback: CallbackQuery):

    user_id = int(callback.data.split(":")[1])

    await callback.bot.send_message(
        chat_id=user_id,
        text=(
            "🎉 Вітаємо!\n\n"
            "Вашу оплату підтверджено.\n\n"
            "Доступ до курсу відкрито!"
        )
    )

    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.answer("Оплату підтверджено.")
    
async def reject_payment(callback: CallbackQuery):

    user_id = int(callback.data.split(":")[1])

    await callback.bot.send_message(
        chat_id=user_id,
        text=(
            "❌ На жаль, ми не змогли підтвердити оплату.\n\n"
            "Будь ласка, перевірте квитанцію або зв'яжіться з нами."
        )
    )

    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.answer("Оплату відхилено.")