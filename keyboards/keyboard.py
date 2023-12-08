from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def main_menu_keyboard():
    keyboard = InlineKeyboardBuilder(
        [
            [
                InlineKeyboardButton(text="Коктейль дня", callback_data=f"random_cocktail")
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