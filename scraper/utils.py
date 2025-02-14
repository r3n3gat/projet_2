import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import os
import pandas as pd

def make_absolute_url(relative_url, base_url='https://books.toscrape.com/'):
    return base_url + relative_url if not relative_url.startswith('http') else relative_url

def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except HTTPError as http_err:
        print(f"[ERREUR] Erreur HTTP : {http_err} pour l'URL {url}")
    except Exception as err:
        print(f"[ERREUR] Erreur : {err} pour l'URL {url}")
    return None

def save_data(data, filepath):
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False, encoding='utf-8')

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Répertoire {directory} créé.")

def parse_category_page(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    book_links = [article.find('h3').find('a')['href'] for article in soup.find_all('article', class_='product_pod')]
    return book_links
