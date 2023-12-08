from fractions import Fraction
from queries.translate_queries import translate_text

async def convert_oz_to_ml(oz_amount):
    try:
        # Try to convert the amount directly to float
        return f"{float(oz_amount) * 30:.2f} ml"
    except ValueError:
        # If it's not a simple float, attempt to parse it as a fraction
        try:
            fraction = Fraction(oz_amount)
            # Your conversion logic here
            # For simplicity, let's assume 1 oz = 30 ml
            ml_amount = float(fraction) * 30
            return f"{ml_amount:.2f} ml"
        except ValueError:
            # If it's neither a float nor a valid fraction, return the original value
            return oz_amount

async def format_ingredient_list(ingredient_list):
    formatted_list = []

    for name, amount in ingredient_list:
        translated_name = await translate_text(name)
        translated_amount = await translate_text(amount)
        if 'oz' in amount:
            # Extract the numerical part from the amount
            numerical_value = amount.split()[0]

            # Convert ounces to milliliters
            ml_amount = await convert_oz_to_ml(numerical_value)
            translated_amount = await translate_text(ml_amount)

            formatted_entry = f"{chr(0x2022)} {translated_name}({name}): {translated_amount}"
            formatted_list.append(formatted_entry)
        else:
            formatted_entry = f"{chr(0x2022)} {translated_name}({name}): {translated_amount}"
            formatted_list.append(formatted_entry)

    formatted_string = "\n".join(formatted_list)
    return formatted_string
