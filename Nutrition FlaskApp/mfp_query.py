import requests
import re
import json
from bs4 import BeautifulSoup

base_url = 'http://www.myfitnesspal.com/food/search?search='
secondary_url = 'https://www.myfitnesspal.com/food/calories/'
def search(query):
	query = query.replace(' ','%20')
	query = query.replace('&','') # don't want & in get query parameters
	url = base_url + query
	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'lxml')
	food_ids = re.findall("calories/(\d+)",str(soup))
	food = {}
	for food_id in food_ids[:5]:
		resp = requests.get(secondary_url+food_id)
		soup2 = BeautifulSoup(resp.content, 'lxml')
		name = soup2.find("h3", {"class": "pageTitle-_5t9X"}).getText()
		calories = soup2.find("h1", {"class": "title-cgZqW"}).getText()
		servings = soup2.find("div", {"class": "jss105"}).getText()
		nutrition_info = soup2.findAll("div", {"class": "NutritionalInfoContainer-3XIjH"})
		data = re.findall("(\w+)<span>(?<=>)(.*?)(?=<)", str(nutrition_info))
		# [('Carbs', '14'), ('Fiber', '2'), ('Sugar', '1'), ('Fat', '18'), ('Saturated', '2'), ('Trans', '0'), ('Protein', '41'), ('Sodium', '1460'), ('Cholesterol', '115'), ('A', '0'), ('C', '8'), ('Calcium', '4'), ('Iron', '8')]
		info = {}
		info['calories'] = calories
		info['servings'] = servings
		info['macros'] = {}
		info['Vitamins'] = {}
		info['macros']['Tot. Carb.'] = data[0][1]
		info['macros']['Dietary Fiber'] = data[1][1]
		info['macros']['Sugars'] = data[2][1]
		info['macros']['Total Fat'] = data[3][1]
		info['macros']['Sat. Fat.'] = data[4][1]
		info['macros']['Trans Fat'] = data[7][1]
		info['macros']['Protein'] = data[8][1]
		info['macros']['Sodium'] = data[9][1]
		info['macros']['Cholesterol'] = data[11][1]
		info['Vitamins']['a'] = data[12][1]
		info['Vitamins']['c'] = data[13][1]
		info['Vitamins']['calcium'] = data[14][1]
		info['Vitamins']['Iron'] = data[15][1]
		food[name] = info
	with open('test.json','w') as f:
		f.write(json.dumps(food))
	return food

# Carbs
# Fiber
# Sugar
# Fat
# Saturated
# Polyunsaturated
# Monounsaturated
# Trans
# Protein
# Sodium
# Potassium
# Cholesterol
# A
# C
# Calcium
# Iron

search('chick fil a nuggets')