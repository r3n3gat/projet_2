import pandas as pd
import os
import requests


def create_output_directory(base_folder='collected_data'):
    """
    Crée le dossier horodaté avec les sous-dossiers book_data et book_image.

    Args:
        base_folder (str): Dossier principal où les données sont stockées.

    Returns:
        dict: Dictionnaire contenant les chemins des sous-dossiers.
    """
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    base_path = os.path.join(base_folder, timestamp)

    # Création des dossiers : principal, book_data et book_image
    book_data_folder = os.path.join(base_path, 'book_data')
    book_image_folder = os.path.join(base_path, 'book_image')

    os.makedirs(book_data_folder, exist_ok=True)
    os.makedirs(book_image_folder, exist_ok=True)

    return {
        'base_path': base_path,
        'book_data_folder': book_data_folder,
        'book_image_folder': book_image_folder
    }


def save_to_csv(data_list, category_name, folders):
    """
    Sauvegarde les données d'une catégorie dans un fichier CSV.

    Args:
        data_list (list): Liste des dictionnaires de données.
        category_name (str): Nom de la catégorie.
        folders (dict): Dictionnaire des chemins des dossiers.
    """
    sanitized_category = category_name.replace(' ', '_').lower()
    file_path = os.path.join(folders['book_data_folder'], f"{sanitized_category}.csv")

    df = pd.DataFrame(data_list)
    df.to_csv(file_path, index=False)

    print(f"[SAUVEGARDE] Données sauvegardées pour la catégorie '{category_name}' dans {file_path}")


def save_image(image_url, book_title, category_name, folders):
    """
    Télécharge et sauvegarde l'image du livre dans un sous-dossier correspondant à la catégorie.

    Args:
        image_url (str): URL de l'image à télécharger.
        book_title (str): Titre du livre pour nommer le fichier.
        category_name (str): Nom de la catégorie pour organiser les images.
        folders (dict): Dictionnaire des chemins des dossiers.
    """
    # Création du sous-dossier pour la catégorie dans book_image
    category_folder = os.path.join(folders['book_image_folder'], category_name.replace(' ', '_').lower())
    os.makedirs(category_folder, exist_ok=True)

    # Nettoyage du titre pour éviter les caractères spéciaux dans le nom du fichier
    sanitized_title = "".join(c if c.isalnum() else "_" for c in book_title)
    file_path = os.path.join(category_folder, f"{sanitized_title}.jpg")

    # Téléchargement de l'image
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
       #print(f"[SAUVEGARDE] Image sauvegardée pour le livre '{book_title}' dans {file_path}")
    else:
        print(f"[ERREUR] Échec du téléchargement de l'image pour '{book_title}'")
