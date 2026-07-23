from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from keyboards import get_courses_menu

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
            style="success",
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
