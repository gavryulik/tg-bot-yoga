from aiogram.types import Message
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext

from states import Form
from keyboards import get_main_menu, get_format_menu
from .courses import send_course

async def cmd_start(message: Message):
    await message.answer_video_note(
        video_note="DQACAgIAAxkBAAMLalevFd4EZrLKB6eh8B6zB0CnyxMAAjOcAAINGrhKJ8MGvTU7htw9BA"
    )
    await message.answer(
        "Привіт! 👋\nЯ — помічник Валентини. Оберіть послугу:",
        reply_markup=get_main_menu()
    )
    
async def deep_link_start(
    message: Message,
    command: CommandObject,
    state: FSMContext,
):
    if command.args:

        arg = command.args

        # ---------- КУРСИ ----------
        if arg.startswith("course_"):

            code = arg.replace("course_", "")

            if code in (
                "pregnant",
                "spine",
                "hormonal",
                "chakra",
            ):
                await send_course(message, code)
                return

        # ---------- ПРАКТИКИ ----------
        elif arg.startswith("practice_"):

            code = arg.replace("practice_", "")

            services = {
                "hatha": "Ха-тха йога",
                "pregnant": "Йога для вагітних",
                "sound": "Sound Healing",
            }

            service = services.get(code)

            if service:

                await state.update_data(chosen_yoga=service)

                if code == "sound":
                    await state.set_state(Form.name)

                    await message.answer(
                        "Дякую! Як до вас звертатися? (Введіть ім'я)"
                    )
                else:
                    await state.set_state(Form.format)

                    await message.answer(
                        "Оберіть формат:",
                        reply_markup=get_format_menu()
                    )

                return

    await cmd_start(message)