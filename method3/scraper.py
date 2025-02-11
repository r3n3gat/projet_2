# method2/scraper.py
import requests
from bs4 import BeautifulSoup
import os


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
            full_link = os.path.join(base_url, relative_link)
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
                link = book.find('a')['href'].replace('../../../', 'https://books.toscrape.com/catalogue/')
                book_links.append(link)

            next_button = soup.find('li', class_='next')
            if next_button:
                next_page = next_button.find('a')['href']
                category_url = os.path.join(os.path.dirname(category_url), next_page)
            else:
                category_url = None
        else:
            print(
                f"[ERREUR] Échec de la récupération des livres pour {category_url} (Status Code: {response.status_code}).")
            break

    return book_links
