from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import AiogramError
from decouple import config

from queries.cocktail_queries import get_random_cocktail, fetch_ingredients
from queries.translate_queries import translate_text

from database_connection import insert_cocktail, delete_cocktail, get_favourite_cocktails
from .other_functions import format_ingredient_list
from keyboards.keyboard import continue_search_keyboard, \
    change_generate_cocktail_button, \
    list_favourite_cocktails, \
    ingredients_keyboard
from states.user_states import UserStates

router = Router()
bot = Bot(config("TOKEN"), parse_mode="HTML")


@router.callback_query(lambda callback: callback.data in ("random_cocktail", "next_cocktail"))
async def handle_random_cocktail(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    
    inline_message_id = callback_query.inline_message_id
    await callback_query.message.edit_reply_markup(inline_message_id, await change_generate_cocktail_button())
    
    cocktail_to_send = await get_random_cocktail()
    
    ingredients = await format_ingredient_list(cocktail_to_send["ingredients"])
    print(cocktail_to_send['recipe'])
    recipe =  await translate_text(cocktail_to_send["recipe"])
    
    cocktail_to_send.update({'telegram_id': callback_query.from_user.id})
    cocktail_to_send.update({'ingredients': ingredients})
    cocktail_to_send.update({'recipe': recipe})
    
    await state.update_data(cocktail = cocktail_to_send)
    
    text = f"""
&#127864; Коктейль: {cocktail_to_send["name"]}\n
Склад: 
{ingredients}\n
Як приготувати: {recipe}
"""
    if cocktail_to_send['photo'] is None:
        await callback_query.message.answer(text=text, reply_markup=await continue_search_keyboard())
    elif cocktail_to_send['photo'] is not None:
        await callback_query.message.answer_photo(photo=cocktail_to_send['photo'])
        await callback_query.message.answer(text=text, reply_markup=await continue_search_keyboard())
    await callback_query.answer()
    await callback_query.message.delete_reply_markup(inline_message_id)


@router.callback_query(lambda callback: callback.data == "save_cocktail")
async def save_cocktail(callback_query: types.CallbackQuery, state: FSMContext):
    cocktail = await state.get_data()
    if "cocktail" in cocktail.keys():
        cocktail = cocktail['cocktail']
        
        insert_cocktail(
            cocktail['telegram_id'],
            cocktail['name'],
            cocktail['recipe'],
            cocktail['photo'],
            cocktail['ingredients']
        )
        await state.clear()
        await callback_query.answer('Коктейль був успішно збережений!')
    
    else:
        await callback_query.answer('Ви вже додали цей коктейль до улюблених')


@router.callback_query(UserStates.fav_cocktails, lambda callback: callback.data in ("next_page", "previous_page"))
async def save_cocktail(callback_query: types.CallbackQuery, state: FSMContext):
    
    data = await state.get_data()
    page = data['page']
    cocktails = data['cocktails']
    inline_photo_id = str(data['inline_photo_id'])
    inline_message_id = str(data['inline_message_id'])
    
    if callback_query.data == 'next_page':
        page = (page + 1) % (len(cocktails))
    elif callback_query.data == 'previous_page':
        page = (page - 1) % (-len(cocktails))
        
    
    media_photo = types.InputMediaPhoto(media=types.URLInputFile(cocktails[page]['photo']))
    
    text = f"""
&#127864; Коктейль: {cocktails[page]["name"]}\n
Склад: 
{cocktails[page]["ingredients"]}\n
Як приготувати: {cocktails[page]["recipe"]}
"""
    await state.update_data({'page': page})
    await bot.edit_message_media(media_photo, callback_query.from_user.id, inline_photo_id)
    await callback_query.message.edit_text(text=text, inline_message_id=inline_message_id, reply_markup=await list_favourite_cocktails())
    await callback_query.answer()

   
@router.callback_query(UserStates.fav_cocktails, lambda callback: callback.data == 'delete_cocktail_from_favourite')
async def delete_favourite_cocktail(callback_query: types.CallbackQuery, state: FSMContext):
    # Select cocktail from cocktails: [{...}, {...}] list
    data = await state.get_data()
    page = data['page']
    cocktail_id = data['cocktails'][page]['id']
    
    try:
        delete_cocktail(cocktail_id)
        cocktails = get_favourite_cocktails(callback_query.from_user.id)
        await state.update_data({"cocktails": cocktails})
        await callback_query.message.answer("Ви успішно видалили коктейль.")
    except AiogramError:
        await callback_query.message.answer("Виникла помилка. Спробуйте ще раз або пізніше.")
    
    await callback_query.answer()
    

@router.callback_query(lambda callback: callback.data == 'cocktail_from_ingredients')
async def make_cocktail_from_ingredients(callback_query: types.CallbackQuery, state: FSMContext):
    
    page = 0
    await state.update_data({'page': page})
    await state.set_state(UserStates.cocktail_from_ingredients)
    
    keyboard = await ingredients_keyboard(page, await fetch_ingredients())
    await callback_query.message.edit_text('Оберіть складові коктейлю:', reply_markup=keyboard)
    
    await callback_query.answer()


@router.callback_query(UserStates.cocktail_from_ingredients, lambda callback: callback.data in ('ingredients_previous_page', 'ingredients_next_page'))
async def make_cocktail_from_ingredients(callback_query: types.CallbackQuery, state: FSMContext):
    
    data = await state.get_data()
    page = data['page']
    
    if callback_query.data == 'ingredients_next_page':
        page += 1
    elif callback_query.data == 'ingredients_previous_page' and page > 0:
        page -= 1
    
    keyboard = await ingredients_keyboard(page, await fetch_ingredients())
    
    try:
        await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    except AiogramError:
        await callback_query.answer('Це початок списку')
    
    await state.update_data({'page': page})
    await callback_query.answer()


        
    