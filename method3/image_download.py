import requests
from bs4 import BeautifulSoup


def get_image_url(book_url):
    """
    Récupère l'URL de l'image du livre depuis la page produit.

    Args:
        book_url (str): URL de la page produit du livre.

    Returns:
        str: URL absolue de l'image du livre.
    """
    response = requests.get(book_url)
    if response.status_code != 200:
        print(f"[ERREUR] Échec de la récupération de la page du livre: {book_url}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    image_tag = soup.select_one('div.item.active img')

    if image_tag:
        image_relative_url = image_tag.get('src').replace('../../', '')
        image_absolute_url = f"https://books.toscrape.com/{image_relative_url}"
        return image_absolute_url
    else:
        print(f"[ERREUR] Image non trouvée sur la page: {book_url}")
        return None
