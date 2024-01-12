from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command

from states.user_states import UserStates
from keyboards.keyboard import main_menu_keyboard, list_favourite_cocktails
from database_connection import get_favourite_cocktails
from aiogram.types.input_media_photo import InputMediaPhoto


router = Router()

@router.message(CommandStart())
async def send_welcome(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Привіт! Цей бот допоможе вам обрати коктейль для гарного настрою :). Для керування ботом користуйся кнопками',
                         reply_markup=await main_menu_keyboard())
    

@router.message(Command('favourite'))
async def send_favourite_cocktail(message: types.Message, state: FSMContext):
    await state.clear()
    page = 0
    
    cocktails = get_favourite_cocktails(message.from_user.id)
    print(cocktails)
    if len(cocktails) > 0:
    
        await state.set_state(UserStates.fav_cocktails)
        await state.set_data({"page": page,
                            "cocktails": cocktails})
        
        if cocktails[page]['created_by_user'] == True:
            if cocktails[page]['photo'] is not None:
                media_photo = types.InputMediaPhoto(media=cocktails[page]['photo'])
            else:
                media_photo = types.InputMediaPhoto(media=types.FSInputFile("no_cocktail_photo.png"))
        elif cocktails[page]['photo'].startswith("https"):
            media_photo = types.InputMediaPhoto(media=types.URLInputFile(cocktails[page]['photo']))
        
        inline_photo_id = await message.answer_media_group([media_photo])
        inline_photo_id = inline_photo_id[0].message_id
        text = f"""
&#127864; Коктейль: {cocktails[page]["name"]}\n
Склад: 
{cocktails[page]["ingredients"]}\n
Як приготувати: {cocktails[page]["recipe"]}
"""
        await state.update_data({"inline_photo_id": inline_photo_id})
        inline_message_id = await message.answer(text=text, reply_markup=await list_favourite_cocktails())
        await state.update_data({"inline_message_id": inline_message_id.message_id})
    
    else:
        await message.answer('Ви ще не зберегли жодного коктейлю. Покищо.', reply_markup=await main_menu_keyboard())