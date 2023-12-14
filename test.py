from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import executor

API_TOKEN = 'your_bot_api_token'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Define states for the conversation
SELECT_INGREDIENT = 'select_ingredient'


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = get_ingredient_keyboard()
    await message.answer("Please choose an ingredient:", reply_markup=keyboard)
    # Set the initial state for the user
    await SELECT_INGREDIENT.set()


@dp.callback_query_handler(lambda c: c.data.startswith('ingredient_'), state=SELECT_INGREDIENT)
async def toggle_ingredient(callback_query: types.CallbackQuery):
    ingredient = callback_query.data.replace("ingredient_", "")
    selected_ingredient = f"{ingredient} (selected)"

    # Toggle the button text
    new_text = selected_ingredient if "selected" not in callback_query.message.text else ingredient

    keyboard = get_ingredient_keyboard()
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=new_text,
                                reply_markup=keyboard)


def get_ingredient_keyboard():
    ingredients = ["Gin", "Scotch", "Apricot brandy"]  # Replace with your actual list of ingredients

    keyboard = InlineKeyboardMarkup(row_width=1)
    for ingredient in ingredients:
        button_text = f"{ingredient} (selected)" if False else ingredient  # Replace with actual selection status
        button = InlineKeyboardButton(text=button_text, callback_data=f"ingredient_{ingredient}")
        keyboard.add(button)

    return keyboard


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
