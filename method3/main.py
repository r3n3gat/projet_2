# Importation des fonctions depuis les modules locaux
from scraper import get_category_links, get_books_links  # Fonctions pour récupérer les liens des catégories et des livres
from exctractor import extract_book_data  # Fonction pour extraire les informations d'un livre
from saver import create_output_directory, save_to_csv  # Fonctions pour créer un dossier de sortie et sauvegarder les données
import time  # Importation de time pour mesurer le temps d'exécution du script

# Définition de l'URL de base du site à scraper
BASE_URL = 'https://books.toscrape.com/index.html'

def main():
    """
    Fonction principale qui coordonne l'ensemble du processus de scraping :
    1. Récupère les catégories de livres.
    2. Scrape les informations de chaque livre dans chaque catégorie.
    3. Sauvegarde les données extraites dans des fichiers CSV distincts.
    """
    start_time = time.time()  # Enregistrement de l'heure de début pour mesurer la durée totale de l'exécution
    total_books_scraped = 0  # Initialisation du compteur de livres extraits
    errors_encountered = 0  # Initialisation du compteur d'erreurs rencontrées

    # Création du dossier de sortie pour stocker les résultats
    output_folder = create_output_directory()

    # Récupération des liens des catégories à partir de l'URL de base
    category_links = get_category_links(BASE_URL)

    print(f"[INFO] {len(category_links)} catégories trouvées.")  # Affichage du nombre de catégories trouvées

    # Parcours de chaque catégorie pour scraper les livres
    for category_name, category_url in category_links.items():
        print(f"[INFO] Scraping de la catégorie : {category_name}")

        # Récupération des liens de tous les livres dans la catégorie
        book_links = get_books_links(category_url)
        print(f"[INFO] {len(book_links)} livres trouvés dans la catégorie '{category_name}'.")

        # Extraction des données pour chaque livre
        category_data = []
        for book_url in book_links:
            book_data = extract_book_data(book_url)
            if book_data:  # Si les données sont extraites avec succès
                category_data.append(book_data)
                total_books_scraped += 1  # Incrémentation du compteur de livres extraits
            else:
                errors_encountered += 1  # Incrémentation du compteur d'erreurs en cas d'échec d'extraction

        # Sauvegarde des données de la catégorie dans un fichier CSV
        save_to_csv(category_data, category_name, output_folder)

    # Calcul de la durée totale de l'exécution
    total_time = time.time() - start_time
    print(f"\n[INFO] Scraping terminé en {total_time:.2f} secondes.")
    print(f"[INFO] Total des livres extraits : {total_books_scraped}")
    print(f"[INFO] Total des erreurs rencontrées : {errors_encountered}")

if __name__ == "__main__":
    main()  # Exécution de la fonction principale lorsque le script est lancé directement
