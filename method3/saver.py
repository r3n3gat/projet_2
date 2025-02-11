import pandas as pd  # Importation de pandas pour la manipulation et l'exportation des données
import os  # Importation de os pour gérer les chemins de fichiers et les dossiers


# Ce module est responsable de la sauvegarde des données extraites dans des fichiers CSV.
# Il organise les résultats pour chaque catégorie dans des fichiers séparés, facilitant ainsi l'accès et la gestion des données.

# Fonction pour créer un dossier de sortie avec un horodatage unique
def create_output_directory(base_folder='collected_data'):
    from datetime import datetime  # Importation de datetime pour générer l'horodatage
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Formatage de la date et l'heure : AAAA-MM-JJ_HH-MM-SS
    folder_path = os.path.join(base_folder, timestamp)  # Création du chemin complet du dossier avec l'horodatage
    os.makedirs(folder_path, exist_ok=True)  # Création du dossier s'il n'existe pas déjà
    return folder_path  # Retourne le chemin du dossier créé


# Fonction pour sauvegarder les données d'une catégorie dans un fichier CSV
def save_to_csv(data_list, category_name, folder_path):
    # Construction du nom du fichier en remplaçant les espaces par des underscores et en convertissant en minuscules
    filename = f"{folder_path}/{category_name.replace(' ', '_').lower()}.csv"

    df = pd.DataFrame(data_list)  # Conversion de la liste de dictionnaires en DataFrame pandas
    df.to_csv(filename, index=False)  # Exportation de la DataFrame en fichier CSV sans index

    # Message de confirmation dans le terminal pour indiquer la sauvegarde réussie
    print(f"[SAUVEGARDE] Données sauvegardées pour la catégorie '{category_name}' dans {filename}")
