import requests
from bs4 import BeautifulSoup
url = "https://codeavecjonathan.com/res/site_recette/recette.html"
"""
# Lecture des données HTML
f = open('recette.html', 'r')
html_content = f.read()
f.close()
"""
response = requests.get(url)
response.encoding = 'utf-8'
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')

# Le titre de la page HTML
titre_h1 = soup.find('h1')
print('\nLe titre de la page HTML:', titre_h1.text)

# La description
# La méthode 1:
#paragraphe_description = soup.find('p', class_='description')
#print('La description de la recette :', paragraphe_description.text)

# La méthode 2 :
all_div_centre = soup.find_all('div', class_='centre')
if all_div_centre and len(all_div_centre) >= 2:
    paragraphe_description = all_div_centre[1].find('p', class_='description')

if paragraphe_description:
    print('\nLe paragraphe de la description :', paragraphe_description.text)

# Le src de l'image
div_info = soup.find('div', class_='info')
img_info = div_info.find('img')
print("\nLe src de l'image :", img_info['src'])

# La table des infos
table_info = soup.find('table', class_='info')
table_info_tr = table_info.find_all('tr')

table_info_headers = table_info_tr[0].find_all('th')
table_info_data = table_info_tr[1].find_all('td')

print('\nInformations :')
for i in range(len(table_info_headers)):
    print('   ', table_info_headers[i].text, ' : ', table_info_data[i].text)

# Les ingredients
div_ingredients = soup.find('div', class_='ingredients')
liste_ingredients = div_ingredients.find_all('p')

print('\nIngredients :')
for ingredient in liste_ingredients:
    print('   ', ingredient.text)

# La preparation
table_preparation = soup.find('table', class_='preparation')
etapes_preparation = table_preparation.find_all('td', class_='preparation_etape')
print('\nEtapes de preparation :')
for i in range(len(etapes_preparation)):
    print('   ', i+1, '-', etapes_preparation[i].text)
