from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from states.user_states import UserStates 
from keyboards.keyboard import user_add_cocktail_next_step
from handlers.command_handlers import send_favourite_cocktail 

from database_connection import insert_cocktail
router = Router()

@router.message(UserStates.user_add_cocktail_photo, F.photo)
async def get_photo_from_user(message: types.Message, state: FSMContext, skipped=False):
    
    data = await state.get_data()
    cocktail = data['user_cocktail']
    
    if skipped:
        await message.message.answer('Hапишіть назву коктейля:')
        cocktail['photo'] = None
    else:
        photo = message.photo[-1].file_id
        cocktail['photo'] = photo
        
        await state.update_data(user_cocktail=cocktail)
        await state.set_state(UserStates.user_add_cocktail_name)
        
        await message.answer('Фото отримано! Тепер напишіть назву коктейля:', reply_markup=await user_add_cocktail_next_step())
    

@router.message(UserStates.user_add_cocktail_name)
async def get_name_from_user(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    cocktail = data['user_cocktail']
    cocktail_name = message.text
    cocktail['name'] = cocktail_name
    
    await state.update_data(user_cocktail=cocktail)
    await state.set_state(UserStates.user_add_cocktail_ingredients)
    await message.answer(f'Чудова назва, {message.from_user.first_name}!\n\n Перейдемо до ігрeдієнтів. Ви можете написати їх в будь-якому форматі, але я рекомендую наступний:\n\n1) Інгред..\n2) Інгред... і т.д.', reply_markup=await user_add_cocktail_next_step())

    
@router.message(UserStates.user_add_cocktail_ingredients)
async def get_ingedients_from_user(message: types.Message, state: FSMContext, skipped=False):
    
    data = await state.get_data()    
    cocktail = data['user_cocktail']
    
    if skipped:
        await message.message.answer('Hапишіть короткий опис до свого коктейля. Ви також можете пропустити цей крок.', reply_markup=await user_add_cocktail_next_step())    
        cocktail['ingredients'] = None
    else:
        
        cocktail_ingredients = message.text
        cocktail['ingredients'] = cocktail_ingredients
        
        await state.update_data(user_cocktail=cocktail)
        await state.set_state(UserStates.user_add_cocktail_recipe)
        await message.answer('Ну і наостанок - напишіть короткий опис до свого коктейля. Ви також можете пропустити цей крок.', reply_markup=await user_add_cocktail_next_step())


@router.message(UserStates.user_add_cocktail_recipe)
async def get_description_from_user(message: types.Message, state: FSMContext, skipped=True):
    
    data = await state.get_data()
    cocktail = data['user_cocktail']    
        
    if skipped==False:
        cocktail_recipe = message.text
        cocktail['recipe'] = cocktail_recipe
        media_photo = types.InputMediaPhoto(media=cocktail['photo'])
        
        text = f"""
&#127864; Коктейль: {cocktail["name"]}\n
Склад: 
{cocktail["ingredients"]}\n
Як приготувати: {cocktail["recipe"]}
"""
        await message.answer_media_group([media_photo])
        await message.answer(text)
        await message.answer("Ви успішно додали коктейль! Він був збережений у /favourite.")
    
    else:
        cocktail['recipe'] = None   
        if cocktail['photo'] != None:
            media_photo = types.InputMediaPhoto(media=cocktail['photo'])
            await message.message.answer_media_group([media_photo])
        else:
            media_photo = types.InputMediaPhoto(media='')
            await message.message.answer_media_group([media_photo])
        for key, value in cocktail.items():
            if value == None:
                cocktail[key] = "--Інформація відсутня--"
        text = f"""
&#127864; Коктейль: {cocktail["name"]}\n
Склад: 
{cocktail["ingredients"]}\n
Як приготувати: {cocktail["recipe"]}
"""
        
        await message.message.answer(text)
        await message.message.answer("Ви успішно додали коктейль! Він був збережений у /favourite.")
        
    #await message.answer('Щось пішло не так... Спробуйте знову додати коктейль, або поверніться трішки пізніше.')
    insert_cocktail(
            message.from_user.id,
            cocktail['name'],
            cocktail['recipe'],
            cocktail['photo'],
            cocktail['ingredients'],
            created_by_user=True
        )
    
    
