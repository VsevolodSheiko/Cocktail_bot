from aiogram import Router, types

from queries.cocktail_queries import get_random_cocktail
from queries.translate_queries import translate_text


from database_connection import get_all_cocktails
from .other_functions import format_ingredient_list
from keyboards.keyboard import continue_search_keyboard, change_generate_cocktail_button

router = Router()


@router.callback_query(lambda callback: callback.data in ("random_cocktail", "next_cocktail"))
async def handle_random_cocktail(callback_query: types.CallbackQuery):

    inline_message_id = callback_query.inline_message_id

    await callback_query.message.edit_reply_markup(inline_message_id, await change_generate_cocktail_button())
    cocktail_to_send = await get_random_cocktail()
    text = f"""
Коктейль: {cocktail_to_send["name"]}\n
&#127864;Склад: 
{await format_ingredient_list(cocktail_to_send["ingredients"])}\n
Як приготувати: {await translate_text(cocktail_to_send["recipe"])}
"""
    if cocktail_to_send['photo'] is None:
        await callback_query.message.answer(text=text, reply_markup=await continue_search_keyboard())
    elif cocktail_to_send['photo'] is not None:
        await callback_query.message.answer_photo(photo=cocktail_to_send['photo'])
        await callback_query.message.answer(text=text, reply_markup=await continue_search_keyboard())
    elif cocktail_to_send['video'] is not None:
        await callback_query.message.answer_video(video=cocktail_to_send['video'])
        await callback_query.message.answer(text=text, reply_markup=await continue_search_keyboard())
    await callback_query.answer()
    await callback_query.message.delete_reply_markup(inline_message_id)


@router.callback_query(lambda callback: callback.data == "save_cocktail")
async def save_random_cocktail(callback_query: types.CallbackQuery):
    