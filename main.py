import requests
from bs4 import BeautifulSoup
import json

# HEADERS pour conternir le problème d'accès à site protégé
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/11'
                          '4.0.0.0 Safari/537.36'}
BASE_URL = 'https://www.cuisine-libre.org/'
JSON_FILENAME = 'recette.json'

def telecharger_et_sauvegarder_image(url):
    response = requests.get(url)
    filename = url.split('/')[-1]
    index_point_interrogation = filename.find('?')
    if index_point_interrogation != -1:
        filename = filename[:index_point_interrogation]
    if response.status_code == 200:
        with open(f'/Users/mouloud/Documents/github/cakeScrap/images_recettes/{filename}', 'wb') as f:
            f.write(response.content)


def nettoyer_texte(t):
   return t.replace('\xa0', ' ').replace('\n', '')


def extraire_duree_recette(recipe_infos_p, nom_class_):
    span = recipe_infos_p.find('span', class_=nom_class_)
    duree = span.find('time').text if span else ""
    return nettoyer_texte(duree).replace('?', '')


def extraire_infos_recette(url):
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Verifier la license
        license_text = soup.find('footer', id='license').text
        license_valide = "cc0" in license_text.lower() or "domaine public" in license_text.lower()
        if not license_valide:
            return print(f"License non valide!")

        # Le titre
        titre = nettoyer_texte(soup.find('h1').contents[0])

        # Les infos
        recipe_infos_p = soup.find('p', id='recipe-infos')
        duree_preparation = extraire_duree_recette(recipe_infos_p, 'duree_preparation')
        duree_cuisson = extraire_duree_recette(recipe_infos_p, 'duree_cuisson')
        duree_repos = extraire_duree_recette(recipe_infos_p, 'duree_repos')
        methode_cuisson_a = recipe_infos_p.find('a')
        methode_cuisson = methode_cuisson_a.text if methode_cuisson_a else ''

        # Une autre façon de faire
        # duree_preparation = recipe_infos_p.find('time', class_=lambda x: x and x.startswith('article-duree_preparation-')).text

        # Les ingredients
        div_ingredients = soup.find('div', id='ingredients')
        ingredients_li = div_ingredients.find_all('li', class_='ingredient')
        ingredients = [nettoyer_texte(ing.text).strip() for ing in ingredients_li if not ing.find('i')]

        # Les etapes de préparation
        div_preparation = soup.find('div', id='preparation')
        etapes = [nettoyer_texte(etape.text).strip() for etape in div_preparation.find_all('p')]
        if not etapes:
            etapes = [nettoyer_texte(etape.text).strip() for etape in div_preparation.find_all('li')]


        # On est obliger de passer par les variables duree_...! à mettre la fct direct dans le dict infos
        infos = {'duree_preparation': duree_preparation,
                 'duree_cuisson': duree_cuisson,
                 'duree_repos': duree_repos,
                 'methode_cuisson': methode_cuisson}

        recette = {'titre': titre,
                   'infos': infos,
                   'ingredients': ingredients,
                   'etapes': etapes}
    else:
        print(f"Erreur status code {response.status_code}")

    #print('Titre :', titre)
    #print('\nInfos :', infos)
    #print('\nRecette', recette)

    return recette


def extraire_liste_recette(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    div_recettes = soup.find('div', id='recettes')
    ul_recettes = div_recettes.find('ul', recursive=False) # Recursive = False pour cherche juste 1er niveau
    li_recettes = ul_recettes.find_all('li')

    #url_recette = url.split('?')
    #recette = extraire_infos_recette(url_recette[0])

    liste_resultats = []
    for li in li_recettes:
        titre = nettoyer_texte(li.find('strong').text)
        a = li.find('a')
        url = BASE_URL + a['href']
        img = a.find('img')
        url_image = BASE_URL + img['src']

        recette = extraire_infos_recette(url)

        if recette:
            liste_resultats.append({'titre': titre, 'url': url, 'url_image': url_image, 'recette': recette})

    return liste_resultats


# extraire_infos_recette('https://www.cuisine-libre.org/gateau-au-chocolat-granuleux')
# extraire_infos_recette('https://www.cuisine-libre.org/tartelettes-aux-myrtilles')
# extraire_infos_recette('https://www.cuisine-libre.org/gateau-au-chocolat-granuleux')
# extraire_infos_recette('https://www.cuisine-libre.org/tourte-de-pommes-de-terre-au-reblochon')

# Charger les données : Texte-->Désérialise le JSON-->données


liste_recettes = extraire_liste_recette('https://www.cuisine-libre.org/boulangerie-et-patisserie?mots%5B%5D=83&max=100')
print(len(liste_recettes))
print(liste_recettes)


# Sauvegarder les données : données-->Sérialise en JSON-->Texte
liste_recettes_json = json.dumps(liste_recettes)
with open(JSON_FILENAME, 'w') as f:
    f.write(liste_recettes_json)


# Téléchargement des images des recettes
#n = 1
#for r in liste_recettes:
#    print(f"Telechargement de l'image de la Recette n° {n}")
#    telecharger_et_sauvegarder_image(r['url_image'])
#   n += 1
