# method3/saver.py
import pandas as pd
import os

def create_output_directory(base_folder='collected_data'):
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    folder_path = os.path.join(base_folder, timestamp)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def save_to_csv(data_list, category_name, folder_path):
    filename = f"{folder_path}/{category_name.replace(' ', '_').lower()}.csv"
    df = pd.DataFrame(data_list)
    df.to_csv(filename, index=False)
    print(f"[SAUVEGARDE] Données sauvegardées pour la catégorie '{category_name}' dans {filename}")
