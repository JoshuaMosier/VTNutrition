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
		optimize = SubmitField('Optimize',id='optimize')

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
		l_list = request.form.getlist('location')
		max_carbs = request.form.get('carbInputName')
		max_fat = request.form.get('total_fatInputName')
		max_protein = request.form.get('proteinInputName')
		max_sugar = request.form.get('sugarInputName')
		max_fiber = request.form.get('fiberInputName')
		max_cholesterol = request.form.get('cholesterolInputName')
		max_iron = request.form.get('ironInputName')
		max_calcium = request.form.get('calciumInputName')
		max_vita = request.form.get('vitaInputName')
		max_vitc = request.form.get('vitcInputName')
		vegetarian = request.form.get('vegetarian')
		vegan = request.form.get('vegan')
		if vegetarian != "*":
			vegetarian = ""
		if vegan != "**":
			vegan = ""
		starting_foods = request.form.getlist('foods')
		if isinstance(starting_foods, list) and len(starting_foods) > 0:
			if isinstance(starting_foods[0], list):
				starting_foods = [starting_foods]
		removed_foods = request.form.getlist('removed_foods')
		if isinstance(removed_foods, list) and len(removed_foods) > 0:
			if isinstance(removed_foods[0], list):
				removed_foods = [removed_foods]
		foods,info,servings = pulp_optimize.get_num_servings(a_list,l_list,int(max_carbs),int(max_fat),int(max_protein),int(max_sugar),int(max_fiber),int(max_cholesterol),int(max_iron),int(max_calcium),int(max_vita),int(max_vitc),vegetarian,vegan,starting_foods,removed_foods)
		status = True
		for item in servings:
			if item < 0 or item%1 != 0:
				foods = []
				info = []
				status = False
		carb_val = max_carbs
		protein_val = max_protein
		fat_val = max_fat
		sugar_val = max_sugar
		fiber_val = max_fiber
		cholesterol_val = max_cholesterol
		iron_val = max_iron
		calcium_val = max_calcium
		vita_val = max_vita
		vitc_val = max_vitc
	else:
		foods = info = []
		max_carbs = max_protein = max_fat = 0
		a_list = []
		# l_list = ['Burger37', 'D2', "Deet's Place", "Owen's/Hokie Grill", 'Turners', 'Vet Med Cafe', 'West End Market', 'DXpress']
		l_list = []
		servings = 0
		status = True
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
		starting_foods = []
		removed_foods = []
	return render_template('index.html',form=form,form_mfp=form_mfp,form_optimize=form_optimize,foods=foods,nutrient_info=info,servings=servings,max_carbs=max_carbs,max_fat=max_fat,max_protein=max_protein,a_list=a_list,l_list=l_list,status=status,carb_val=carb_val, 
		protein_val=protein_val, fat_val=fat_val, sugar_val=sugar_val, fiber_val=fiber_val, cholesterol_val=cholesterol_val, iron_val=iron_val,calcium_val=calcium_val,vita_val=vita_val,vitc_val=vitc_val,vegetarian=vegetarian,vegan=vegan,
		starting_foods=starting_foods,removed_foods=removed_foods)

@app.route("/cron/do_the_thing", methods=['POST'])
def do_the_thing():
    logging.info("Did the thing")
    return "OK", 200
	
if __name__ == '__main__':
		app.run(debug=True)