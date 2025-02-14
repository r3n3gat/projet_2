Bonjour Sam,  

Je vous adresse ce mail afin de vous presenter comme attendu le résultat
de cette mission de scraping.
Je l'ai construite comme un pipeline **ETL (Extract, Transform, Load)** permettant d'extraire
des informations et images de livres depuis le site [Books to Scrape](https://books.toscrape.com).  

Pour des raisons de clarté et maintenabilité, je l'ai construit en modules, ceci permettant 
aussi de facilement le faire évoluer et/ou, si besoin de rajouter d'autres fonctions.

J'ai énormement documenté mon code afin que tout soit facilement comprehensible afin que les
prochains développeurs puissent facilement le maintenir ou l'enrichir.

De plus le fichier README.md est lui aussi détaillé afin d'assurer la prise 
en main du projet.

J'ai aussi mis en place plusieurs affichage console afin de pouvoir deboguer rapidement
et avoir un récapitulatif global du travail effectué.

Je vous fais ici une explication du fonctionnement un peu plus poussée mais concise
pour une future présentation :

###  Fonctionnement :
1. **EXTRACT** :  
   - Récupération automatique des catégories et des liens de chaque livre.  
   - Extraction des données : titre, prix, stock, description, notation, etc.  
   - Téléchargement des images associées.

2. **TRANSFORM** :  
   - Nettoyage et structuration des noms de fichiers. 
   - trnasformation des URL.
   - Classement des livres et images par catégorie.  

3. **LOAD** :  
   - Stockage dans un dossier global `collected_data/` qui, à chaque run, créera un dossier 
   horodaté qui comprendra deux sous-dossiers :
     - `book_data/` → CSV contenant les informations des livres.  
     - `book_image/` → Images des livres triées par catégorie.  

###  Organisation des fichiers :
Chaque run génère un nouveau dossier dans `collected_data/` contenant les données et images.

###  Installation & Exécution :
- Installer Python et les dépendances (`pip install -r requirements.txt`).
- Lancer le script avec `python main.py`.

Ce pipeline peut être facilement adapté pour d'autres sites ou besoins.  
N'hésitez pas à me contacter pour toute question.

Cordialement,  
r3n3gat  
