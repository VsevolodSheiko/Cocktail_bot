from aiogram import Bot, Router, types
from aiogram.filters import CommandStart
from keyboards.keyboard import main_menu_keyboard

router = Router()

@router.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer(text='Привіт! Цей бот допоможе вам обрати коктейль для гарного настрою :). Для керування ботом користуйся кнопками',
                         reply_markup=await main_menu_keyboard())