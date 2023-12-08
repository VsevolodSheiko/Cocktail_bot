import requests


async def get_random_cocktail():
	result = {}

	url_1 = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
	url_2 = "https://www.thecocktaildb.com/api/json/v2/1/random.php"

	response = requests.get(url=url_1)
	response = response.json()['drinks'][0]

	result['name'] = response['strDrink']
	result['video'] = response['strVideo']
	result['recipe'] = response['strInstructions']
	result['photo'] = response['strDrinkThumb']
	
	ingredients = [response[f"strIngredient{i}"] for i in range(1, 16) if response[f"strIngredient{i}"]]
	measures = [response[f"strMeasure{i}"] for i in range(1, 16) if response[f"strMeasure{i}"]]

	# Combine ingredients and measures
	ingredient_measure_pairs = list(zip(ingredients, measures))

	# Print the result
	for pair in ingredient_measure_pairs:
		new_pair = f"{pair[0]}: {pair[1]}"
		pair = new_pair

	result['ingredients'] = ingredient_measure_pairs
	
	return result

