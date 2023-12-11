from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    fav_cocktails = State()
    cocktail_from_ingredients = State()