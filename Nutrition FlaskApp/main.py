from flask import Flask, render_template, request, jsonify
import pulp_optimize
import sys
from wtforms import Form, TextField, SubmitField
import json
import myfitnesspal

app = Flask(__name__)

with open('nutrition_allergen+vitamins.json') as f:
	  locations = json.load(f)

names = set()
cals, fat, sat_fat, trans_fat, cholesterol, sodium, fiber, sugar, protein, carb, calcium, iron, vita, vitc = ([] for i in range(14))

def mfp_query(text):
	return myfitnesspal.search(text)
	# print(myfitnesspal.search("Owen's Cheesesteak"))

for location in locations:
		for foods in locations[location]:
			if float(locations[location][foods]['calories']) > 0:
				names.add(foods + " - " + location)
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

class OptimizeForm(Form):
		optimize = SubmitField('Run Optimization',id='optimize')

class SearchForm(Form):
		autocomp = TextField('Add Food Item',id='autocomplete')

class SearchFormMFP(Form):
		autocomp_mfp = TextField('Add MFP Item',id='autocomplete_mfp')

@app.route('/autocomplete',methods=['GET'])
def autocomplete():
		search = request.args.get('term')
		app.logger.debug(search)
		return jsonify(json_list=sorted(list(names)))

@app.route('/autocomplete_mfp',methods=['GET','POST'])
def autocomplete_mfp():
	data = request.get_data(as_text=True)
	possible_foods = mfp_query(data)
	return jsonify(possible_foods)

@app.route('/', methods=['GET', 'POST'])
def index():
	form = SearchForm(request.form)
	form_mfp = SearchFormMFP(request.form)
	form_optimize = OptimizeForm(request.form)
	# form_optimize = OptimizeForm(request.form)
	if form_optimize.optimize.data and form.validate():
		a_list = request.form.getlist('allergies')
		breakfast = request.form.get('breakfastInputName')
		lunch = request.form.get('lunchInputName')
		dinner = request.form.get('dinnerInputName')
		# meals = [breakfast,lunch,dinner]
		# print(meals)
		num_meals = 0
		if breakfast != 'None':
			num_meals = num_meals+1
		if lunch != 'None':
			num_meals = num_meals+1
		if dinner!= 'None':
			num_meals = num_meals+1
		display_results = True
		display_loc_error = False
		if num_meals == 0:
			display_results = False
			display_loc_error = True
			MF = 0
		else:
			MF = 1/num_meals
		# print('meal factor: ' + str(MF))
		activity = 0
		age = request.form.get('ageInputName')
		height = request.form.get('heightInputName')
		weight = request.form.get('weightInputName')
		gender = request.form.get('genderInputName')
		activity = request.form.get('activityInputName')
		# print(age,height,weight,gender)
		male_activity = [1,1,1.12,1.27,1.54]
		female_activity = [1,1,1.14,1.27,1.45]
		if gender == 'male':
			calories = (66 + (13.7*weight) + (5 * height) - (6.8*age))*male_activity[activity]
			# print(calories)
			brek_max_carbs = int(.55*calories*MF)
			brek_max_fat = int(.25*calories*MF)
			brek_max_protein = int(.20*calories*MF)
			lunch_max_carbs = int(.55*calories*MF)
			lunch_max_fat = int(.25*calories*MF)
			lunch_max_protein = int(.20*calories*MF)
			dinner_max_carbs = int(.55*calories*MF)
			dinner_max_fat = int(.25*calories*MF)
			dinner_max_protein = int(.20*calories*MF)
		elif gender == 'female':
			calories = (655 + (9.6*weight) + (1.8 * height) - (4.7*age))*female_activity[activity]
			brek_max_carbs = int(.55*calories*MF)
			brek_max_fat = int(.25*calories*MF)
			brek_max_protein = int(.20*calories*MF)
			lunch_max_carbs = int(.55*calories*MF)
			lunch_max_fat = int(.25*calories*MF)
			lunch_max_protein = int(.20*calories*MF)
			dinner_max_carbs = int(.55*calories*MF)
			dinner_max_fat = int(.25*calories*MF)
			dinner_max_protein = int(.20*calories*MF)
		else:
			brek_max_carbs = int(200*MF)
			brek_max_fat = int(50*MF)
			brek_max_protein = int(100*MF)
			lunch_max_carbs = int(200*MF)
			lunch_max_fat = int(50*MF)
			lunch_max_protein = int(100*MF)
			dinner_max_carbs = int(200*MF)
			dinner_max_fat = int(50*MF)
			dinner_max_protein = int(100*MF)
		brek_max_sugar = int(request.form.get('sugarInputName'))*MF
		brek_max_fiber = int(request.form.get('fiberInputName'))*MF
		brek_max_cholesterol = int(request.form.get('cholesterolInputName'))*MF
		brek_max_iron = int(request.form.get('ironInputName'))*MF
		brek_max_calcium = int(request.form.get('calciumInputName'))*MF
		brek_max_vita = int(request.form.get('vitaInputName'))*MF
		brek_max_vitc = int(request.form.get('vitcInputName'))*MF
		lunch_max_sugar = int(request.form.get('sugarInputName'))*MF
		lunch_max_fiber = int(request.form.get('fiberInputName'))*MF
		lunch_max_cholesterol = int(request.form.get('cholesterolInputName'))*MF
		lunch_max_iron = int(request.form.get('ironInputName'))*MF
		lunch_max_calcium = int(request.form.get('calciumInputName'))*MF
		lunch_max_vita = int(request.form.get('vitaInputName'))*MF
		lunch_max_vitc = int(request.form.get('vitcInputName'))*MF
		dinner_max_sugar = int(request.form.get('sugarInputName'))*MF
		dinner_max_fiber = int(request.form.get('fiberInputName'))*MF
		dinner_max_cholesterol = int(request.form.get('cholesterolInputName'))*MF
		dinner_max_iron = int(request.form.get('ironInputName'))*MF
		dinner_max_calcium = int(request.form.get('calciumInputName'))*MF
		dinner_max_vita = int(request.form.get('vitaInputName'))*MF
		dinner_max_vitc = int(request.form.get('vitcInputName'))*MF
		vegetarian = request.form.get('vegetarian')
		vegan = request.form.get('vegan')
		if vegetarian != "*":
			vegetarian = ""
		if vegan != "**":
			vegan = ""
		brek_foods = lunch_foods = dinner_foods = []
		brek_info = lunch_info = dinner_info = []
		brek_servings = lunch_servings = dinner_servings = 0
		brek_status = lunch_status = dinner_status = True
		brek_starting_foods = lunch_starting_foods = dinner_starting_foods = []
		brek_removed_foods = lunch_removed_foods = dinner_removed_foods =[]
		brek_info = lunch_info = dinner_info = [0] * 14
		carb_val = protein_val = fat_val = sugar_val = fiber_val = cholesterol_val = iron_val = calcium_val = vita_val = vitc_val = 0
		max_carbs = max_fat = max_protein = 0
		if breakfast != 'None':
			carb_val += brek_max_carbs 
			protein_val += brek_max_protein
			fat_val += brek_max_fat
			sugar_val += brek_max_sugar
			fiber_val += brek_max_fiber
			cholesterol_val += brek_max_cholesterol
			iron_val += brek_max_iron
			calcium_val += brek_max_calcium
			vita_val += brek_max_vita
			vitc_val += brek_max_vitc
			max_carbs += brek_max_carbs
			max_fat += brek_max_fat
			max_protein += brek_max_protein
			brek_starting_foods = request.form.getlist('brek_foods')
			if isinstance(brek_starting_foods, list) and len(brek_starting_foods) > 0:
				if isinstance(brek_starting_foods[0], list):
					brek_starting_foods = [brek_starting_foods]
			brek_removed_foods = request.form.getlist('brek_removed_foods')
			if isinstance(brek_removed_foods, list) and len(brek_removed_foods) > 0:
				if isinstance(brek_removed_foods[0], list):
					brek_removed_foods = [brek_removed_foods]
			brek_foods,brek_info,brek_servings = pulp_optimize.get_num_servings(a_list,breakfast,int(brek_max_carbs),int(brek_max_fat),int(brek_max_protein),int(brek_max_sugar),int(brek_max_fiber),int(brek_max_cholesterol),int(brek_max_iron),int(brek_max_calcium),int(brek_max_vita),int(brek_max_vitc),vegetarian,vegan,brek_starting_foods,brek_removed_foods)
			brek_status = True
			for item in brek_servings:
				if item < 0 or item%1 != 0:
					brek_foods = []
					brek_info = []
					brek_status = False
		if lunch != 'None':
			carb_val += lunch_max_carbs 
			protein_val += lunch_max_protein
			fat_val += lunch_max_fat
			sugar_val += lunch_max_sugar
			fiber_val += lunch_max_fiber
			cholesterol_val += lunch_max_cholesterol
			iron_val += lunch_max_iron
			calcium_val += lunch_max_calcium
			vita_val += lunch_max_vita
			vitc_val += lunch_max_vitc
			max_carbs += lunch_max_carbs
			max_fat += lunch_max_fat
			max_protein += lunch_max_protein
			lunch_starting_foods = request.form.getlist('lunch_foods')
			if isinstance(lunch_starting_foods, list) and len(lunch_starting_foods) > 0:
				if isinstance(lunch_starting_foods[0], list):
					lunch_starting_foods = [lunch_starting_foods]
			lunch_removed_foods = request.form.getlist('lunch_removed_foods')
			if isinstance(lunch_removed_foods, list) and len(lunch_removed_foods) > 0:
				if isinstance(lunch_removed_foods[0], list):
					lunch_removed_foods = [lunch_removed_foods]
			lunch_foods,lunch_info,lunch_servings = pulp_optimize.get_num_servings(a_list,lunch,int(lunch_max_carbs),int(lunch_max_fat),int(lunch_max_protein),int(lunch_max_sugar),int(lunch_max_fiber),int(lunch_max_cholesterol),int(lunch_max_iron),int(lunch_max_calcium),int(lunch_max_vita),int(lunch_max_vitc),vegetarian,vegan,lunch_starting_foods,lunch_removed_foods)
			lunch_status = True
			for item in lunch_servings:
				if item < 0 or item%1 != 0:
					lunch_foods = []
					lunch_info = []
					lunch_status = False
		if dinner != 'None':
			carb_val += dinner_max_carbs 
			protein_val += dinner_max_protein
			fat_val += dinner_max_fat
			sugar_val += dinner_max_sugar
			fiber_val += dinner_max_fiber
			cholesterol_val += dinner_max_cholesterol
			iron_val += dinner_max_iron
			calcium_val += dinner_max_calcium
			vita_val += dinner_max_vita
			vitc_val += dinner_max_vitc
			max_carbs += dinner_max_carbs
			max_fat += dinner_max_fat
			max_protein += dinner_max_protein
			dinner_starting_foods = request.form.getlist('dinner_foods')
			if isinstance(dinner_starting_foods, list) and len(dinner_starting_foods) > 0:
				if isinstance(dinner_starting_foods[0], list):
					dinner_starting_foods = [dinner_starting_foods]
			dinner_removed_foods = request.form.getlist('dinner_removed_foods')
			if isinstance(dinner_removed_foods, list) and len(dinner_removed_foods) > 0:
				if isinstance(dinner_removed_foods[0], list):
					dinner_removed_foods = [dinner_removed_foods]
			dinner_foods,dinner_info,dinner_servings = pulp_optimize.get_num_servings(a_list,dinner,int(dinner_max_carbs),int(dinner_max_fat),int(dinner_max_protein),int(dinner_max_sugar),int(dinner_max_fiber),int(dinner_max_cholesterol),int(dinner_max_iron),int(dinner_max_calcium),int(dinner_max_vita),int(dinner_max_vitc),vegetarian,vegan,dinner_starting_foods,dinner_removed_foods)
			dinner_status = True
			for item in dinner_servings:
				if item < 0 or item%1 != 0:
					dinner_foods = []
					dinner_info = []
					dinner_status = False
		info = [0] * 14
		nutrient_headers = ['Calories: ', 'Total Fat: ', 'Protein: ', 'Carbohydrates: ', 'Saturated Fat: ', 'Trans Fat: ', 'Cholesterol: ', 'Fiber: ', 'Sugars: ', 'Calcium: ', 'Iron: ', 'Vitamin A: ', 'Vitamin C: ', 'Sodium: ']
		brek_tmp = lunch_tmp = dinner_tmp = 0
		for i in range(14):
			if brek_info[i] != 0:
				brek_tmp = float(brek_info[i].split(' ')[-1])
			if lunch_info[i] != 0:
				lunch_tmp = float(brek_info[i].split(' ')[-1])
			if dinner_info[i] != 0:
				dinner_tmp = float(brek_info[i].split(' ')[-1])
			info[i] = nutrient_headers[i] + str(round((brek_tmp + lunch_tmp + dinner_tmp),1))
	else:
		brek_foods = brek_info = lunch_foods = lunch_info = dinner_foods = dinner_info =[]
		max_carbs = max_protein = max_fat = 0
		a_list = []
		# l_list = ['Burger37', 'D2', "Deet's Place", "Owen's/Hokie Grill", 'Turners', 'Vet Med Cafe', 'West End Market', 'DXpress']
		breakfast = False
		lunch = False
		dinner = False
		brek_servings = lunch_servings = dinner_servings = 0
		brek_status = lunch_status = dinner_status = True
		carb_val = 200
		protein_val = 100
		fat_val = 50
		sugar_val = 50
		fiber_val = 30
		cholesterol_val = 300
		iron_val = 100
		calcium_val = 100
		vita_val = 100
		vitc_val = 100
		vegetarian = ""
		vegan = ""
		brek_starting_foods = lunch_starting_foods = dinner_starting_foods = []
		brek_removed_foods = lunch_removed_foods = dinner_removed_foods = []
		max_carbs = 200
		max_fat = 50
		max_protein = 100
		display_results = False
		display_loc_error = False
		info = []
	return render_template('test.html',
	form=form,form_mfp=form_mfp,form_optimize=form_optimize,
	brek_foods=brek_foods,
	nutrient_info=info,
	brek_servings=brek_servings,
	lunch_foods=lunch_foods,
	lunch_servings=lunch_servings,
	dinner_foods=dinner_foods,
	dinner_servings=dinner_servings,
	a_list=a_list,
	max_carbs = max_carbs,
	max_fat = max_fat,
	max_protein = max_protein,
	brek_status=brek_status,
	lunch_status=lunch_status,
	dinner_status=dinner_status,
	carb_val=int(carb_val), protein_val=int(protein_val), fat_val=int(fat_val), sugar_val=int(sugar_val), fiber_val=int(fiber_val), cholesterol_val=int(cholesterol_val), 
	iron_val=int(iron_val),calcium_val=int(calcium_val),vita_val=int(vita_val),vitc_val=int(vitc_val),vegetarian=vegetarian,vegan=vegan,
	breakfast=breakfast,lunch=lunch,dinner=dinner,
	display_results = display_results,
	display_loc_error=display_loc_error)

if __name__ == '__main__':
		app.run(debug=True)