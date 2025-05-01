import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import psycopg2


def get_db_connection():
    return psycopg2.connect("dbname=kimdur user=postgres password=8002")



def add_user(chat_id, first_name, last_name, phone):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users(chat_id, first_name, last_name, phone) VALUES (%s, %s, %s, %s)",
            (chat_id, first_name, last_name, phone)
        )
        conn.commit()
        return True
    except psycopg2.IntegrityError:

        return False
    finally:
        cur.close()
        conn.close()



class RegistrationForm(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()



TOKEN = "yhjgjhgjhg"



dp = Dispatcher()



@dp.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"Assalomu alaykum, {message.from_user.full_name}!\n"
        f"Ro'yxatdan o'tish uchun ismingizni kiriting:"
    )
    await state.set_state(RegistrationForm.first_name)



@dp.message(RegistrationForm.first_name)
async def handle_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Familiyangizni kiriting:")
    await state.set_state(RegistrationForm.last_name)



@dp.message(RegistrationForm.last_name)
async def handle_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer("Telefon raqamingizni kiriting (+998XXXXXXXXX formatida):")
    await state.set_state(RegistrationForm.phone)



@dp.message(RegistrationForm.phone)
async def handle_phone(message: types.Message, state: FSMContext):
    phone = message.text



    if not phone.startswith('+998') or len(phone) != 13 or not phone[1:].isdigit():
        await message.answer("❗️ Telefon raqam noto‘g‘ri formatda. To‘g‘ri kiriting: +998XXXXXXXXX")
        return


    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")

    if add_user(message.from_user.id, first_name, last_name, phone):
        await message.answer(
            f"✅ Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!\n\n"
            f"<b>Ism:</b> {first_name}\n"
            f"<b>Familiya:</b> {last_name}\n"
            f"<b>Telefon:</b> {phone}",
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer("⚠️ Siz avval ro'yxatdan o'tgansiz!")

    await state.clear()



async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
