import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os  # Pour gérer les dossiers et chemins

# Fonction pour envoyer une requête HTTP et récupérer le contenu
def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Erreur {response.status_code} lors de la récupération de la page.")
        return None

# Fonction pour extraire les informations du produit
def extract_product_info(url):
    page_content = get_page_content(url)

    if page_content:
        soup = BeautifulSoup(page_content, "html.parser")

        # Extraction des informations
        product_info = {}

        product_info['product_page_url'] = url
        product_info['universal_product_code'] = soup.find('th', string='UPC').find_next('td').text.strip()
        product_info['title'] = soup.find('h1').text.strip()
        product_info['price_including_tax'] = soup.find('th', string='Price (incl. tax)').find_next('td').text.strip()
        product_info['price_excluding_tax'] = soup.find('th', string='Price (excl. tax)').find_next('td').text.strip()
        product_info['number_available'] = soup.find('th', string='Availability').find_next('td').text.strip()
        product_info['product_description'] = soup.find('meta', attrs={'name': 'description'})['content'].strip()[:30]
        product_info['category'] = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
        product_info['review_rating'] = soup.find('p', class_='star-rating')['class'][1]  # star-rating: 'One', 'Two', etc.
        product_info['image_url'] = soup.find('img')['src']

        return product_info
    return None

def save_to_csv(product_info, folder="collected_data", filename_base="product_data"):
    # Créer le dossier s'il n'existe pas
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Dossier '{folder}' créé.")

    # Ajouter un horodatage au nom du fichier
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format : 20250128_143015
    filename = f"{filename_base}_{timestamp}.csv"

    # Chemin complet du fichier (dans le dossier collected_data)
    file_path = os.path.join(folder, filename)

    # Vérifier si le fichier CSV existe déjà
    try:
        df = pd.read_csv(file_path)
        # Vérifier si l'URL du produit existe déjà dans le CSV
        if product_info['product_page_url'] in df['product_page_url'].values:
            print("Produit déjà enregistré.")
            return
    except FileNotFoundError:
        df = pd.DataFrame()

    # Ajouter les nouvelles données
    new_row = pd.DataFrame([product_info])
    df = pd.concat([df, new_row], ignore_index=True)

    # Sauvegarder dans le fichier CSV
    df.to_csv(file_path, index=False)
    print(f"Fichier sauvegardé sous le nom : {file_path}")


# Fonction principale pour récupérer et enregistrer les données
def scrape_data():
    url = "https://books.toscrape.com/catalogue/soumission_998/index.html"  # Exemple d'URL de produit
    product_info = extract_product_info(url)

    if product_info:
        print(f"Produit trouvé: {product_info['title']}")
        save_to_csv(product_info)  # Sauvegarde les données dans le CSV
    else:
        print("Impossible d'extraire les informations du produit.")

if __name__ == "__main__":
    scrape_data()
