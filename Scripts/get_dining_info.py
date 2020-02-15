# Base URL: http://foodpro.dsa.vt.edu/menus/MenuAtLocation.aspx?locationNum=16&naFlag=1

# Location #s
# 	18 - Burger 37
# 	15 - D2
# 	07 - Deet's
# 	13 - DX
# 	09 - Owen's/Hokie Grill
# 	14 - Turners
# 	19 - Vet Med Cafe
# 	16 - West End

import datetime
from datetime import date
import urllib.request
import re
import json
from bs4 import BeautifulSoup

dining_locations = {"Burger37":'18',"D2":'15',"Deet's Place":'07',"DXpress":'13',"Owen's/Hokie Grill":'09',"Turners":'14',"Vet Med Cafe":'19',"West End Market":'16'}
# url = ('http://foodpro.dsa.vt.edu/menus/MenuAtLocation.aspx?locationNum=16&naFlag=1')

def get_dining_info(locs,info_date):
	f = open("Menu_"+info_date[0]+"-"+info_date[1]+"-"+info_date[2]+".txt", "w")
	for value in locs:
		f.write(str(value) + "\n")
		url = 'http://foodpro.dsa.vt.edu/menus/MenuAtLocation.aspx?locationNum=' + locs[value] +'&naFlag=1&myaction=read&dtdate='+info_date[0]+'%2f'+info_date[1] +'%2f'+info_date[2]
		nutrition_info = urllib.request.urlopen(url)
		soup = BeautifulSoup(nutrition_info,'html.parser')
		food_items = re.findall("(label\\..*)(\"\\s+)", str(soup))
		for item in food_items:
			f.write(item[0].replace("\"","").replace("amp;","") + "\n")
	f.close()

def get_todays_menu():
	today = date.today()
	info_date = [str(today.month),str(today.day),str(today.year)]
	get_dining_info(dining_locations, info_date)

def get_custom_menu():
	
