# method2/scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

#Ce module est chargé de récupérer les liens des catégories et des livres sur le site Books to Scrape

# Fonction pour obtenir les liens des catégories à partir de la page d'accueil
def get_category_links(base_url):  # base_url est l'URL de la page principale du site
    response = requests.get(base_url)  # Effectue une requête GET pour récupérer le contenu de la page

    if response.ok:  # Vérifie si la requête a réussi (code 200)
        soup = BeautifulSoup(response.content, 'html.parser')  # Analyse le contenu HTML avec BeautifulSoup

        # Trouve la section contenant la liste des catégories
        category_section = soup.find('ul', class_='nav nav-list')

        # Récupère tous les liens des catégories, en ignorant le premier qui correspond à "Books" (toutes catégories)
        categories = category_section.find_all('a')[1:]

        category_links = {}  # Dictionnaire pour stocker les noms et URLs des catégories

        for category in categories:  # Boucle sur chaque catégorie trouvée
            name = category.text.strip()  # Récupère le nom de la catégorie et enlève les espaces inutiles
            relative_link = category['href']  # Récupère le lien relatif de la catégorie

            # Construit le lien complet en joignant l'URL de base avec le lien relatif
            full_link = urljoin(base_url, relative_link)

            # Ajoute la catégorie et son lien complet au dictionnaire
            category_links[name] = full_link

        return category_links  # Retourne le dictionnaire des catégories et leurs liens

    else:
        # Affiche un message d'erreur si la requête échoue
        print(f"[ERREUR] Impossible de récupérer les catégories (Status Code: {response.status_code}).")
        return {}  # Retourne un dictionnaire vide en cas d'erreur



# Fonction pour obtenir les liens des livres d'une catégorie
def get_books_links(category_url):  # category_url est l'URL de la page d'une catégorie
    book_links = []  # Liste pour stocker les liens des livres

    while category_url:  # Continue tant qu'il y a des pages à parcourir dans la catégorie
        response = requests.get(category_url)  # Effectue une requête GET pour récupérer la page de la catégorie

        if response.ok:  # Vérifie si la requête est réussie (code 200)
            soup = BeautifulSoup(response.content, 'html.parser')  # Analyse le contenu HTML avec BeautifulSoup

            # Trouve tous les livres sur la page
            books = soup.find_all('h3')

            for book in books:  # Boucle sur chaque livre trouvé
                # Récupère le lien relatif du livre et le transforme en lien absolu
                link = urljoin(category_url, book.find('a')['href'])
                book_links.append(link)  # Ajoute le lien complet à la liste des livres

            # Vérifie s'il y a une page suivante
            next_button = soup.find('li', class_='next')

            if next_button:  # S'il y a un bouton "next", récupère le lien de la page suivante
                next_page = next_button.find('a')['href']
                category_url = urljoin(category_url, next_page)  # Met à jour l'URL pour continuer la boucle
            else:
                category_url = None  # Pas de page suivante, arrêt de la boucle

        else:
            # Affiche un message d'erreur si la requête échoue
            print(f"[ERREUR] Échec de la récupération des livres pour {category_url} (Status Code: {response.status_code}).")
            break  # Arrête la boucle en cas d'erreur

    return book_links  # Retourne la liste des liens de tous les livres dans la catégorie

