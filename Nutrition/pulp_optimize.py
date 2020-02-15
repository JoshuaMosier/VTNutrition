import pulp
import json
import re
def get_num_servings(a_list,l_list,max_carbs,max_fat,max_protein,max_sugar,max_fiber,max_cholesterol,max_iron,max_calcium,max_vita,max_vitc,vegetarian,vegan,starting_foods,removed_foods):
	with open('nutrition_allergen+vitamins.json') as f:
	  locations = json.load(f)

	diet_model = pulp.LpProblem("The Diet Problem", pulp.LpMinimize)

	names, cals, fat, sat_fat, trans_fat, cholesterol, sodium, fiber, sugar, protein, carb, calcium, iron, vita, vitc = ([] for i in range(15))

	allergens = ["Milk","Eggs","Fish","Crustacean Shellfish","Tree Nuts","Peanuts","Wheat","Soybeans","Gluten"]

	init_cals, init_fat, init_cholesterol, init_fiber, init_sugar, init_protein, init_carbs, init_calcium, init_iron, init_vita, init_vitc, init_satfat, init_transfat, init_sodium = (0 for i in range(14))
	for item in starting_foods:
		# for item in locations:
		out = re.findall("(\\d.\\d+)\\sservings of (.*)\\s\\-\\s(.*)",item)[0]
		fd = locations[out[2]][out[1]]
		init_cals += float(fd['calories'])*int(float(out[0]))
		init_carbs += float(fd['macros']['Tot. Carb.'])*int(float(out[0]))
		init_fat += float(fd['macros']['Total Fat'])*int(float(out[0]))
		init_fat += float(fd['macros']['Sat. Fat'])*int(float(out[0]))
		init_fat += float(fd['macros']['Trans Fat'])*int(float(out[0]))
		init_sodium += float(fd['macros']['Sodium'])*int(float(out[0]))
		init_cholesterol += float(fd['macros']['Cholesterol'])*int(float(out[0]))
		init_fiber += float(fd['macros']['Dietary Fiber'])*int(float(out[0]))
		init_sugar += float(fd['macros']['Sugars'])*int(float(out[0]))
		init_protein += float(fd['macros']['Protein'])*int(float(out[0]))
		init_calcium += float(fd['Vitamins']['calcium'])*int(float(out[0]))
		init_iron += float(fd['Vitamins']['iron'])*int(float(out[0]))
		init_vita += float(fd['Vitamins']['a'])*int(float(out[0]))
		init_vitc += float(fd['Vitamins']['c'])*int(float(out[0]))

	removed = []
	for item in removed_foods:
		out = re.findall("(\\d.\\d+)\\sservings of (.*)\\s\\-\\s(.*)",item)[0]
		removed.append(out[1])
		# print(str(int(float(out[0]))) + " " + str(locations[out[2]][out[1]]['macros']['Tot. Carb.']) + " " + str(init_carbs))

	starting = []
	for item in starting_foods:
		out = re.findall("(\\d.\\d+)\\sservings of (.*)\\s\\-\\s(.*)",item)[0]
		starting.append(out[1])

	# dining_locations = {"Burger37":'18',"D2":'15',"Deet's Place":'07',"DXpress":'13',"Owen's/Hokie Grill":'09'
	# ,"Turners":'14',"Vet Med Cafe":'19',"West End Market":'16'}
	for location in locations:
		for foods in locations[location]:
			if float(locations[location][foods]['calories']) > 50 and location in l_list and a_list not in locations[location][foods]['allergens'] and vegetarian in foods and vegan in foods and foods not in starting and foods not in removed:
				names.append(foods + " - " + location)
				f = locations[location][foods]
				cals.append(float(f['calories']))
				fat.append(float(f['macros']['Total Fat']))
				sat_fat.append(float(f['macros']['Sat. Fat']))
				trans_fat.append(float(f['macros']['Trans Fat']))
				cholesterol.append(float(f['macros']['Cholesterol']))
				sodium.append(float(f['macros']['Sodium']))
				fiber.append(float(f['macros']['Dietary Fiber']))
				sugar.append(float(f['macros']['Sugars']))
				protein.append(float(f['macros']['Protein']))
				carb.append(float(f['macros']['Tot. Carb.']))
				calcium.append(float(f['Vitamins']['calcium']))
				iron.append(float(f['Vitamins']['iron']))
				vita.append(float(f['Vitamins']['a']))
				vitc.append(float(f['Vitamins']['c']))

	x = pulp.LpVariable.dict("x_%s", names, lowBound = 0, upBound = 4, cat=pulp.LpInteger)

	calories = dict(zip(names, cals))
	carbs = dict(zip(names, carb))
	fats = dict(zip(names, fat))
	sat_fats = dict(zip(names, sat_fat))
	trans_fats = dict(zip(names, trans_fat))
	proteins = dict(zip(names, protein))
	salts = dict(zip(names, sodium))
	sugars = dict(zip(names, sugar))
	fibers = dict(zip(names, fiber))
	chols = dict(zip(names, cholesterol))
	irons = dict(zip(names, iron))
	vitas = dict(zip(names, vita))
	vitcs = dict(zip(names, vitc))
	calcs = dict(zip(names, calcium))

	diet_model += sum([calories[i] * x[i] for i in names])
	diet_model += sum([proteins[i]*x[i] for i in names]) >= (max_protein - init_protein)
	diet_model += sum([fats[i]*x[i] for i in names]) >= (max_fat - init_fat)
	diet_model += sum([sugars[i]*x[i] for i in names]) >= (max_sugar - init_sugar)
	# diet_model += sum([salts[i]*x[i] for i in names]) <= 2300
	diet_model += sum([carbs[i]*x[i] for i in names]) >= (max_carbs - init_carbs)
	diet_model += sum([sat_fats[i]*x[i] for i in names]) >= 0
	diet_model += sum([trans_fats[i]*x[i] for i in names]) >= 0
	diet_model += sum([fibers[i]*x[i] for i in names]) >= (max_fiber - init_fiber)
	diet_model += sum([chols[i]*x[i] for i in names]) >= (max_cholesterol - init_cholesterol)
	diet_model += sum([irons[i]*x[i] for i in names]) <= (max_iron - init_iron)
	diet_model += sum([vitas[i]*x[i] for i in names]) <= (max_vita - init_vita)
	diet_model += sum([vitcs[i]*x[i] for i in names]) <= (max_vitc - init_vitc)
	diet_model += sum([calcs[i]*x[i] for i in names]) <= (max_calcium - init_calcium)
	# diet_model += sum([irons[i]*x[i] for i in names]) >= 100
	# diet_model += sum([vitas[i]*x[i] for i in names]) >= 100
	# diet_model += sum([vitcs[i]*x[i] for i in names]) >= 100
	# diet_model += sum([calcs[i]*x[i] for i in names]) >= 100

	diet_model.solve()

	selected_foods = []
	servings = []
	for food in names:
		if x[food].value() != 0:
			selected_foods.append("%s servings of %s"%(x[food].value(),food))
			servings.append(x[food].value())
	cal=init_cals
	f=init_fat
	sf=init_satfat
	tf=init_transfat
	ch=init_cholesterol
	fi=init_fiber
	su=init_sugar
	pr=init_protein
	car=init_carbs
	calc=init_calcium
	ir=init_iron
	vitamina=init_vita
	vitaminc=init_vitc
	sod=init_sodium
	for food in names:
		cal += x[food].value()*calories[food]
		pr += x[food].value()*proteins[food]
		f += x[food].value()*fats[food]
		su += x[food].value()*sugars[food]
		sod += x[food].value()*salts[food]
		car += x[food].value()*carbs[food]
		sf += x[food].value()*sat_fats[food]
		tf += x[food].value()*trans_fats[food]
		ch += x[food].value()*chols[food]
		calc += x[food].value()*calcs[food]
		ir += x[food].value()*irons[food]
		vitamina += x[food].value()*vitas[food]
		vitaminc += x[food].value()*vitcs[food]
		fi += x[food].value()*fibers[food]

	nutrient_information = []
	nutrient_information.append("Calories: " + str(round(cal,4)))
	nutrient_information.append("Total Fat: " + str(round(f,4)))
	nutrient_information.append("Protein: " +  str(round(pr,4)))
	nutrient_information.append("Carbohydrates: " + str(round(car,4)))
	nutrient_information.append("Saturated Fat: " + str(round(sf,4)))
	nutrient_information.append("Trans Fat: " + str(round(tf,4)))
	nutrient_information.append("Cholesterol: " + str(round(ch,4)))
	nutrient_information.append("Fiber: " + str(round(fi,4)))
	nutrient_information.append("Sugars: " + str(round(su,4)))
	nutrient_information.append("Calcium: " + str(round(calc,4)))
	nutrient_information.append("Iron: " + str(round(ir,4)))
	nutrient_information.append("Vitamin A: " + str(round(vitamina,4)))
	nutrient_information.append("Vitamin C: " + str(round(vitaminc,4)))
	nutrient_information.append("Sodium: " + str(round(sod,4)))

	return [selected_foods,nutrient_information,servings]