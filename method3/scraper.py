# method2/scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_category_links(base_url):
    response = requests.get(base_url)
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        category_section = soup.find('ul', class_='nav nav-list')
        categories = category_section.find_all('a')[1:]  # Ignorer "Books"

        category_links = {}
        for category in categories:
            name = category.text.strip()
            relative_link = category['href']
            full_link = urljoin(base_url, relative_link)  # Correction ici
            category_links[name] = full_link

        return category_links
    else:
        print(f"[ERREUR] Impossible de récupérer les catégories (Status Code: {response.status_code}).")
        return {}


def get_books_links(category_url):
    book_links = []

    while category_url:
        response = requests.get(category_url)
        if response.ok:
            soup = BeautifulSoup(response.content, 'html.parser')
            books = soup.find_all('h3')
            for book in books:
                relative_link = book.find('a')['href']
                book_url = urljoin(category_url, relative_link)  # Correction ici
                book_links.append(book_url)

            next_button = soup.find('li', class_='next')
            if next_button:
                next_page = next_button.find('a')['href']
                category_url = urljoin(category_url, next_page)  # Correction ici
            else:
                category_url = None
        else:
            print(f"[ERREUR] Échec de la récupération des livres pour {category_url} (Status Code: {response.status_code}).")
            break

    return book_links
