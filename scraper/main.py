# Importation des fonctions depuis les modules locaux
from scraper import get_category_links, get_books_links  # Fonctions pour récupérer les liens des catégories et des livres
from extractor import extract_book_data  # Fonction pour extraire les informations d'un livre
from image_download import get_image_url  # Fonction pour récupérer l'URL de l'image
from saver import create_output_directory, save_to_csv, save_image  # Fonctions pour créer des dossiers et sauvegarder données/images
import time  # Pour mesurer le temps d'exécution du script

# Définition de l'URL de base du site à scraper
BASE_URL = 'https://books.toscrape.com/index.html'


def main():
    """
    Fonction principale qui :
    1. Récupère les catégories de livres.
    2. Scrape les informations de chaque livre dans chaque catégorie.
    3. Télécharge les images de chaque livre.
    4. Sauvegarde les données extraites dans des fichiers CSV distincts.
    """
    start_time = time.time()  # Enregistrement de l'heure de début pour mesurer la durée totale de l'exécution
    total_books_scraped = 0  # Compteur de livres extraits
    errors_encountered = 0  # Compteur d'erreurs rencontrées

    # Création du dossier horodaté avec les sous-dossiers book_data et book_image
    output_folders = create_output_directory()

    # Récupération des liens des catégories
    category_links = get_category_links(BASE_URL)
    print(f"[INFO] {len(category_links)} catégories trouvées.")  # Affichage du nombre de catégories trouvées

    # Parcours de chaque catégorie pour scraper les livres
    for category_name, category_url in category_links.items():
        print(f"[INFO] Scraping de la catégorie : {category_name}")

        # Récupération des liens de tous les livres dans la catégorie
        book_links, errors = get_books_links(category_url)
        print(f"[INFO] {len(book_links)} livres trouvés dans la catégorie '{category_name}'.")

        # Extraction des données et téléchargement des images pour chaque livre
        category_data = []
        for book_url in book_links:
            try:
                # Extraction des données du livre
                book_data = extract_book_data(book_url)

                # Récupération de l'image
                image_url = get_image_url(book_url)
                if image_url:
                    save_image(image_url, book_data['title'], category_name, output_folders)

                category_data.append(book_data)
                total_books_scraped += 1  # Incrémentation du compteur de livres extraits

            except Exception as e:
                print(f"[ERREUR] Exception lors de l'extraction des données pour {book_url}: {e}")
                errors_encountered += 1  # Incrémentation du compteur d'erreurs en cas d'échec

        # Sauvegarde des données de la catégorie dans un fichier CSV
        save_to_csv(category_data, category_name, output_folders)

    # Calcul de la durée totale de l'exécution
    total_time = time.time() - start_time
    print(f"\n[INFO] Scraping terminé en {total_time:.2f} secondes.")
    print(f"[INFO] Total des livres extraits : {total_books_scraped}")
    print(f"[INFO] Total des erreurs rencontrées : {errors_encountered}")


if __name__ == "__main__":
    main()  # Exécution de la fonction principale lorsque le script est lancé directement
