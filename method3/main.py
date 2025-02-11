# method3/main.py
from method3.scraper import get_category_links, get_books_links
from method3.exctractor import get_product_info
from method3.saver import create_output_directory, save_to_csv


def main():
    base_url = 'https://books.toscrape.com/'
    categories = get_category_links(base_url)

    folder_path = create_output_directory()

    total_categories = 0
    total_books = 0
    errors = []

    for category_name, category_url in categories.items():
        print(f"[INFO] Scraping de la catégorie : {category_name}")
        total_categories += 1

        book_links = get_books_links(category_url)
        print(f"[INFO] {len(book_links)} livres trouvés dans la catégorie '{category_name}'.")

        products_data = []
        for link in book_links:
            product_info = get_product_info(link)
            if product_info:
                products_data.append(product_info)
                total_books += 1
            else:
                errors.append(link)

        if products_data:
            save_to_csv(products_data, category_name, folder_path)
        else:
            print(f"[ATTENTION] Aucune donnée sauvegardée pour la catégorie '{category_name}'.")

    # Résumé des résultats
    print("\n--- RÉCAPITULATIF DU SCRAPING ---")
    print(f"Nombre total de catégories scannées : {total_categories}")
    print(f"Nombre total de livres scannés : {total_books}")
    if errors:
        print(f"[ERREURS] {len(errors)} erreurs rencontrées.")
        for error in errors:
            print(f"  - Échec pour : {error}")
    else:
        print("[SUCCÈS] Aucun problème rencontré.")


if __name__ == "__main__":
    main()
