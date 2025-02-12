import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin



# Fonction pour extraire les informations d'un livre à partir de sa page produit
def extract_book_data(book_url):  # book_url est l'URL de la page du livre
    response = requests.get(book_url)  # Effectue une requête GET pour récupérer le contenu de la page

    if response.ok:  # Vérifie si la requête a réussi (status code 200)
        soup = BeautifulSoup(response.content, 'html.parser')  # Analyse le contenu HTML avec BeautifulSoup

        # Extraction des informations depuis le tableau des détails
        product_info = soup.find('table', class_='table table-striped').find_all('td')
        upc = product_info[0].text  # Universal Product Code (UPC)
        price_incl_tax = float(product_info[3].text[1:])  # Prix TTC (on enlève le symbole £ et convertit en float)
        price_excl_tax = float(product_info[2].text[1:])  # Prix HT (on enlève le symbole £ et convertit en float)
        number_available = int(product_info[5].text.split(' ')[2].strip('('))  # Nombre d'exemplaires disponibles

        # Titre du livre
        title = soup.find('h1').text

        # Description du livre (si disponible)
        description_tag = soup.find('meta', attrs={'name': 'description'})
        product_description = description_tag['content'].strip() if description_tag else "Pas de description"

        # Catégorie du livre
        category = soup.find('ul', class_='breadcrumb').find_all('a')[2].text.strip()

        # Note de l'avis (évaluation)
        rating_tag = soup.find('p', class_='star-rating')
        review_rating = rating_tag['class'][1] if rating_tag else "Aucune note"

        # URL de l'image du livre (convertie en URL absolue)
        image_relative_url = soup.find('img')['src'].replace('../../', '')
        image_url = urljoin(book_url, image_relative_url)

        # Création d'un dictionnaire pour stocker les données extraites
        return {
            'product_page_url': book_url,
            'universal_product_code': upc,
            'title': title,
            'price_including_tax': price_incl_tax,
            'price_excluding_tax': price_excl_tax,
            'number_available': number_available,
            'product_description': product_description,
            'category': category,
            'review_rating': review_rating,
            'image_url': image_url
        }

    else:
        # Affiche un message d'erreur si la page n'est pas accessible
        print(f"[ERREUR] Impossible de récupérer les données pour {book_url} (Status Code: {response.status_code}).")
        return {}  # Retourne un dictionnaire vide en cas d'erreur
