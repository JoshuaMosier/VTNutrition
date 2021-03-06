import requests
from bs4 import BeautifulSoup
import urllib.request
import time
import re
import json
from datetime import date

def get_dining_nutrition_json(filename):
	with open('Menus/'+filename) as f:
		lines = f.readlines()

	def parse_html(html):
		dict_food = {}
		soup = BeautifulSoup(html,'html.parser')
		if soup.find(id="serving_size_container") != None and soup.find(id="recipe_title") != None:
			dict_food["serving"] = re.search("\\d\\s([^\\s]+)",soup.find(id="serving_size_container").get_text().replace("\r\n","")).group(0)
			dict_food["calories"] = re.findall("\\d+",soup.find(id="calories_container").get_text().replace("\r\n",""))[0]
			daily_info = soup.find_all("div", {"class": "daily_value"})
			macros = {}
			for info in daily_info:
				macros[" ".join(re.findall("([\\w.-]+)",info.find("div").find_all("div")[0].getText())[:-1])] = re.findall("([\\w.-]+)",info.find("div").find_all("div")[0].getText())[-1]
			dict_food["macros"] = macros
			list_allergens = re.findall("(ALLERGENS:</strong>)(.*)",str(soup))[0][1].replace(" ","").replace("\r","").split(",")
			if len(list_allergens) == 0:
				dict_food["allergens"] = None		
			else:
				dict_food["allergens"] = list_allergens
			list_vitamins = re.findall("(<span class=\"iron_percent\">)(\\d+)",str(soup))
			# print(str(list_vitamins) + "      " + str(soup.find(id="recipe_title").get_text().replace("\r\n","").strip()))
			vit = {}
			calcium = re.findall("(Calcium <span class=\"iron_percent\">)(\\d+)",str(soup))
			iron = re.findall("(Iron <span class=\"iron_percent\">)(\\d+)",str(soup))
			vita = re.findall("(Vitamin A - IU <span class=\"iron_percent\">)(\\d+)",str(soup))
			vitc = re.findall("(Vitamin C <span class=\"iron_percent\">)(\\d+)",str(soup))
			if len(calcium) == 0:
				vit['calcium'] = 0
			else:
				vit['calcium'] = calcium[0][1]
			if len(iron) == 0:
				vit['iron'] = 0
			else:	
				vit['iron'] = iron[0][1]
			if len(vita) == 0:
				vit['a'] = 0
			else:
				vit['a'] = vita[0][1]
			if len(vitc) == 0:
				vit['c'] = 0
			else:
				vit['c'] = vitc[0][1]
			dict_food["Vitamins"] = vit
			return dict_food,soup.find(id="recipe_title").get_text().replace("\r\n","").strip()
		else:
			return None

	large_food_dict = {}
	unqiue_dining_hall = {}
	for i,line in enumerate(lines):
		if line.startswith('label') == False:
			location = line.replace("\n","")
			large_food_dict[location] = {}
		else:
			url = ('http://foodpro.dsa.vt.edu/menus/' + line)
			nutrition_info = urllib.request.urlopen(url)
			food = parse_html(nutrition_info)
			if food != None:
				large_food_dict[location][food[1]] = food[0]

	
	with open('/Menu_Json/' + filename + 'json', 'w') as fp:
		json.dump(large_food_dict, fp)

get_dining_nutrition_json('Menu_2-14-2020.txt')