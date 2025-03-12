import asyncio
import random
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import add_marker_to_db, check_marker_exists, get_all_markers, increment_delete_requests, \
    delete_marker_from_db

API_TOKEN = '7557459871:AAFaC0VZbnVO6Dq0UwyCR3s_tpnGCoNyNrk'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

router = Router()
dp.include_router(router)


# Buttons
def get_inline_buttons():
    buttons = [
        [InlineKeyboardButton(text="Добавить метку", callback_data="add_marker")],
        [InlineKeyboardButton(text="Показать карту", callback_data="show_map")],
        [InlineKeyboardButton(text="Удалить метку", callback_data="delete_marker")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Command handler to show buttons
@router.message(Command('start'))
async def start(message: types.Message):
    await message.answer("Привет! Выберите действие:", reply_markup=get_inline_buttons())


# Callback handlers
@router.callback_query(F.data == 'add_marker')
async def add_marker(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Пожалуйста, отправьте свою геолокацию.")


@router.message(F.location)
async def handle_location(message: types.Message):
    user_id = message.from_user.id
    latitude = message.location.latitude
    longitude = message.location.longitude

    if check_marker_exists(latitude, longitude):
        await message.answer("В этом месте уже стоит метка!")
    else:
        add_marker_to_db(latitude, longitude, user_id)
        await message.answer("Метка добавлена!", reply_markup=get_inline_buttons())


@router.callback_query(F.data == 'show_map')
async def show_map(callback_query: types.CallbackQuery):
    unique_id = random.randint(1000, 9999)  # Unique ID for the map
    await bot.send_message(callback_query.from_user.id,
                           f"Вот ваша карта: http://localhost:5000/map/{unique_id}",
                           reply_markup=get_inline_buttons())


@router.callback_query(F.data == 'delete_marker')
async def delete_marker(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Введите ID метки для удаления.")


@router.message()
async def delete_marker_request(message: types.Message):
    marker_id = message.text.strip()
    try:
        marker_id = int(marker_id)

        marker = get_all_markers(marker_id)
        if marker:
            increment_delete_requests(marker_id)
            delete_requests = marker[0][4]

            if delete_requests >= 3:
                delete_marker_from_db(marker_id)
                await message.answer("Метка удалена.")
            else:
                await message.answer("Запрос на удаление принят.", reply_markup=get_inline_buttons())
        else:
            await message.answer("Метка с таким ID не найдена.", reply_markup=get_inline_buttons())

    except ValueError:
        await message.answer("Пожалуйста, введите корректный ID метки.")


# Start Aiogram bot
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
