import requests

async def serialize_cocktail(cocktail: dict):
	result = {}

	result['name'] = cocktail['strDrink']
	result['video'] = cocktail['strVideo']
	result['recipe'] = cocktail['strInstructions']
	result['photo'] = cocktail['strDrinkThumb']
	
	ingredients = [cocktail[f"strIngredient{i}"] for i in range(1, 16) if cocktail[f"strIngredient{i}"]]
	measures = [cocktail[f"strMeasure{i}"] for i in range(1, 16) if cocktail[f"strMeasure{i}"]]

	# Combine ingredients and measures
	ingredient_measure_pairs = list(zip(ingredients, measures))

	# Print the result
	for pair in ingredient_measure_pairs:
		new_pair = f"{pair[0]}: {pair[1]}"
		pair = new_pair

	result['ingredients'] = ingredient_measure_pairs
	
	return result



async def get_random_cocktail():

	url_1 = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
	url_2 = "https://www.thecocktaildb.com/api/json/v2/1/random.php"

	response = requests.get(url=url_2)
	response = response.json()['drinks'][0]

	result = await serialize_cocktail(response)
	
	return result


async def fetch_ingredients():
    
    url = 'https://www.thecocktaildb.com/api/json/v2/1/list.php?i=list'
    
    response = requests.get(url=url)
    data = response.json()['drinks']
    
    return data


async def search_cocktails_from_ingredients(str_of_ingredients):

	cocktails_ids = [] 
	url = f'https://www.thecocktaildb.com/api/json/v2/1/filter.php?i={str_of_ingredients}'

	response = requests.get(url=url)

	data = response.json()['drinks']
	if data != "None Found":
		for cocktail in data:
			cocktails_ids.append(cocktail['idDrink'])
		return cocktails_ids
	else:
		return data


async def search_cocktail_by_id(cocktail_id):

	url = f'https://www.thecocktaildb.com/api/json/v2/1/lookup.php?i={cocktail_id}'

	response = requests.get(url=url)

	response = response.json()['drinks'][0]
	result = await serialize_cocktail(response)
	
	return result
