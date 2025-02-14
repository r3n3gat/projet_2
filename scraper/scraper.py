import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_category_links(base_url):
    """
    Cette fonction récupère les liens de toutes les catégories de livres à partir de la page d'accueil du site.

    Paramètre :
    - base_url (str) : L'URL de la page d'accueil du site "Books to Scrape".

    Retour :
    - category_links (dict) : Un dictionnaire contenant le nom des catégories comme clés et leurs URL complètes comme valeurs.
    """

    # Envoyer une requête HTTP GET à l'URL de base pour récupérer le contenu de la page.
    response = requests.get(base_url)

    # Vérifier si la requête a réussi (code 200).
    if response.ok:
        # Parser le contenu HTML de la page avec BeautifulSoup.
        soup = BeautifulSoup(response.content, 'html.parser')

        # Trouver la section de la page qui contient les catégories de livres (balise <ul> avec les classes 'nav nav-list').
        category_section = soup.find('ul', class_='nav nav-list')

        # Extraire tous les liens (<a>) des catégories. On ignore le premier lien qui est "Books" (lien général).
        categories = category_section.find_all('a')[1:]

        # Initialiser un dictionnaire pour stocker les noms et les liens des catégories.
        category_links = {}

        # Parcourir chaque lien de catégorie pour extraire son nom et construire son URL complète.
        for category in categories:
            name = category.text.strip()  # Récupérer le nom de la catégorie en supprimant les espaces inutiles.
            relative_link = category['href']  # Récupérer le lien relatif de la catégorie.
            full_link = urljoin(base_url, relative_link)  # Convertir le lien relatif en lien absolu avec urljoin.
            category_links[name] = full_link  # Ajouter le nom et le lien de la catégorie au dictionnaire.

        return category_links  # Retourner le dictionnaire contenant les catégories et leurs liens.

    else:
        # Si la requête a échoué, afficher un message d'erreur avec le code de statut.
        print(f"[ERREUR] Impossible de récupérer les catégories (Status Code: {response.status_code}).")
        return {}  # Retourner un dictionnaire vide en cas d'erreur.


def get_books_links(category_url):
    """
    Cette fonction récupère tous les liens des pages produits des livres appartenant à une catégorie spécifique.
    Elle gère également la pagination pour récupérer les livres répartis sur plusieurs pages.

    Paramètre :
    - category_url (str) : L'URL de la catégorie de livres.

    Retour :
    - book_links (list) : Une liste contenant les URL complètes des pages produits de tous les livres de la catégorie.
    """

    # Initialiser une liste vide pour stocker les liens des livres.
    book_links = []


    # Boucle pour parcourir toutes les pages de la catégorie (pagination).
    while category_url:
        # Envoyer une requête HTTP GET pour récupérer le contenu de la page de la catégorie.
        response = requests.get(category_url)

        # Vérifier si la requête a réussi (code 200).
        if response.ok:
            # Parser le contenu HTML de la page avec BeautifulSoup.
            soup = BeautifulSoup(response.content, 'html.parser')

            # Trouver tous les titres de livres dans la page (balises <h3> contiennent les liens des livres).
            books = soup.find_all('h3')

            # Parcourir chaque livre pour extraire son lien.
            for book in books:
                # Récupérer le lien relatif de la page produit du livre.
                relative_link = book.find('a')['href']

                # Corriger le lien relatif pour obtenir un lien absolu en remplaçant le chemin.
                absolute_link = relative_link.replace('../../../', 'https://books.toscrape.com/catalogue/')

                # Ajouter le lien absolu à la liste des liens de livres.
                book_links.append(absolute_link)

            # Vérifier s'il existe un bouton "Next" pour passer à la page suivante.
            next_button = soup.find('li', class_='next')
            if next_button:
                # Récupérer le lien de la page suivante.
                next_page = next_button.find('a')['href']

                # Construire l'URL complète de la page suivante.
                category_url = urljoin(category_url, next_page)
            else:
                # Si aucune page suivante, sortir de la boucle.
                category_url = None
        else:
            # Si la requête échoue, afficher un message d'erreur avec le code de statut.
            print(
                f"[ERREUR] Échec de la récupération des livres pour {category_url} (Status Code: {response.status_code}).")

            # Sortir de la boucle en cas d'erreur.
            break

    # Retourner la liste des liens de livres.
    return book_links


def main():
    base_url = 'https://books.toscrape.com/'
    category_links = get_category_links(base_url)
    total_books = total_errors = 0
    book_count_per_category = {}

    for category_name, category_url in category_links.items():
        print(f"Scraping de la catégorie : {category_name}")
        book_titles, errors = get_books_links(category_url)
        total_books += len(book_titles)
        book_count_per_category[category_name] = len(book_titles)
        total_errors += len(errors)
        print(f"{len(book_titles)} livres trouvés dans la catégorie '{category_name}'.")
        if errors:
            print("Erreurs rencontrées:")
            for error in errors:
                print(error)

    print(f"\n--- Récapitulatif ---")
    print(f"Nombre total de livres : {total_books}")
    print(f"Erreurs rencontrées : {total_errors}")

if __name__ == "__main__":
    main()