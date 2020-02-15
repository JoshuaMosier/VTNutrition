import requests
import soupselect
from bs4 import BeautifulSoup
import re

base_url = 'http://www.myfitnesspal.com/food/search?search='

def search(query):
    query = query.replace(' ','%20')
    query = query.replace('&','') # don't want & in get query parameters
    url = base_url + query
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    products = []
    food_descriptions = soupselect.select(soup, 'div.food_description')
    for food_description in food_descriptions:
        try:
            anchors = soupselect.select(food_description, 'a')
            match = re.search(">.+<\/a>",str(anchors[0]))
            name = match.group(0).replace('</a>','').replace('>','')
            match = re.search(">.+<\/a>",str(anchors[1]))
            brand = match.group(0).replace('</a>','').replace('>','')
            product = {}
            product['name'] = name
            product['brand'] = brand
            products.append(product)
        except:
            pass

    index=0
    nutritional_info = soupselect.select(soup, 'div.nutritional_info')
    nutritional_data = soupselect.select(soup, 'div.nutritional_facts')
    print(requests.get('https://www.myfitnesspal.com/food/search?search=chick%20fil%20a%20nuggets').text)
    for nutrition in nutritional_info:
        try:
            product = products[index]
            matches=re.finditer("<label>.+<\/label>.+(,|[\s|\t|\n]*<\/div>)",str(nutrition))
            for match in matches:
                s = match.group(0)
                label = s[:s.index('</label>')]
                label = label.replace('<label>','').replace(':','').strip()
                label_value = s[s.index("</label>"):]
                label_value = label_value.replace('</label>','').replace(',','').replace('</div>','').strip()
                product[label] = label_value
            index += 1
        except:
            pass
    return products[:5]