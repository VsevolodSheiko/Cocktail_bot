from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    fav_cocktails = State()
    cocktail_from_ingredients = State()
    
    user_add_cocktail_photo = State()
    user_add_cocktail_name = State()
    user_add_cocktail_ingredients = State()
    user_add_cocktail_recipe = State()