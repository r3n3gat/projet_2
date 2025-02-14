# Projet 2 : scraper Python

## Prérequis

Avant de commencer, assurez-vous d'avoir Python et un environnement virtuel
configuré sur votre machine.

### Installation des dépendances

1. Clonez le repository si ce n'est pas déjà fait :
   
   git clone https://github.com/r3n3gat/projet-2.git

   
2. Utiliser le fichier `requirements.txt`

   faites dans votre terminal : pip install -r requirements.txt


3. Créer un environnement virtuel :

   python -m venv env 

   env\Scripts\activate ( sur windows )

   env\Scripts\activate  ( dur Mac ou Linux )


4. Lancer le script principal ( main )

   python main.py


5. Résultats du script :

   Les fichiers sont générés dans collected_data/ avec un dossier horodaté contenant :

book_data/ → CSV des livres par catégorie

book_image/ → Images des livres classées par catégorie

_______________________________________________________________________ 


Ce projet suit un pipeline ETL (Extract, Transform, Load) :

Extract  :

Récupération des catégories et des liens des livres (scraper.py).

Extraction des données (extractor.py).

Récupération des images (image_download.py).


Transform  :

Nettoyage des données.

Formatage des noms de fichiers.

Organisation des fichiers et images.


Load  :

Sauvegarde des CSV et images dans un dossier structuré (saver.py).


### Voila vous pouvez commencez à travailler sur ce projet



CONTACT : r3n3gat sur r3n3gat@hotmail.com

