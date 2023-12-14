from aiogram.types import InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def main_menu_keyboard():
    keyboard = InlineKeyboardBuilder(
        [
            [
                InlineKeyboardButton(text="Коктейль дня", callback_data=f"random_cocktail"),
                InlineKeyboardButton(text="Коктейль з інгредієнтів", callback_data=f"cocktail_from_ingredients"),
            ]
        ]
    )
    return keyboard.adjust(1).as_markup()


async def continue_search_keyboard():
    keyboard = InlineKeyboardBuilder(
        [
            [
                InlineKeyboardButton(text="Наступний", callback_data=f"next_cocktail"),
                InlineKeyboardButton(text="Зберегти", callback_data=f"save_cocktail"),
                
            ]
        ]
    )
    return keyboard.adjust(1).as_markup()


async def change_generate_cocktail_button():
    keyboard = InlineKeyboardBuilder(
        [
            [
                InlineKeyboardButton(text="\U0001F378 Готуємо коктейльчик...", callback_data=f"change_button")
            ]
        ]
    )
    return keyboard.adjust(1).as_markup()


async def list_favourite_cocktails():
    keyboard = InlineKeyboardBuilder(
        [
            [
                InlineKeyboardButton(text="\U0000274C Видалити з улюблених", callback_data=f"delete_cocktail_from_favourite"),
                InlineKeyboardButton(text="\U000023EA", callback_data=f"previous_page"),
                InlineKeyboardButton(text="\U000023E9", callback_data=f"next_page")
            ]
        ]
    )
    return keyboard.adjust(1, 2).as_markup()


async def ingredients_keyboard(current_page, ingredients_list, state: FSMContext=None):
    buttons_list = []

    if state != None:
        buttons_status = await state.get_data()
        if 'selected_buttons' in buttons_status:
            buttons_status = buttons_status['selected_buttons']
        else:
           buttons_status = []
    else:
        buttons_status = []

    start_index = current_page * 8
    end_index = start_index + 8

    for ingredient in ingredients_list[start_index:end_index]:
        ingredient_name = ingredient['strIngredient1']
        if ingredient_name in buttons_status:
            button = InlineKeyboardButton(text=f'{ingredient_name} \U00002705', callback_data=f"ingredient_{ingredient_name}")
        else:
            button = InlineKeyboardButton(text=ingredient_name, callback_data=f"ingredient_{ingredient_name}")
        
        buttons_list.append(button)

    buttons_list.append(InlineKeyboardButton(text="\U000023EA", callback_data="ingredients_previous_page"))
    buttons_list.append(InlineKeyboardButton(text="\U000023E9", callback_data="ingredients_next_page"))
    buttons_list.append(InlineKeyboardButton(text="Знайти коктейль", callback_data="find_cocktail_from_ingredients"))
    keyboard = InlineKeyboardBuilder([buttons_list])
    
    return keyboard.adjust(2, 2, 2, 2, 2, 1).as_markup()


async def toggle_ingredient_button():
    keyboard = InlineKeyboardBuilder(
        [
            [
                InlineKeyboardButton(text="\U000023EA", callback_data=f"previous_page_cocktail"),
                InlineKeyboardButton(text="\U000023E9", callback_data=f"next_page_cocktail")
            ]
        ]
    )
    return keyboard.adjust(2).as_markup()