# method2/extractor.py
import requests
from bs4 import BeautifulSoup
from method3.utils import clean_price, clean_stock, make_absolute_url


def get_product_info(url):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Nettoyage et transformation des données
        price_incl = clean_price(soup.find('th', string='Price (incl. tax)').find_next('td').text)
        price_excl = clean_price(soup.find('th', string='Price (excl. tax)').find_next('td').text)
        availability = clean_stock(soup.find('th', string='Availability').find_next('td').text)

        image_relative_url = soup.find('img')['src']
        image_url = make_absolute_url(image_relative_url)

        product_info = {
            'product_page_url': url,
            'universal_product_code': soup.find('th', string='UPC').find_next('td').text.strip(),
            'title': soup.find('h1').text.strip(),
            'price_including_tax': price_incl,
            'price_excluding_tax': price_excl,
            'number_available': availability,
            'product_description': soup.find('meta', attrs={'name': 'description'})['content'].strip(),
            'category': soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip(),
            'review_rating': soup.find('p', class_='star-rating')['class'][1],
            'image_url': image_url
        }

        return product_info
    else:
        print(f"[ERREUR] Impossible de récupérer le produit {url} (Status Code: {response.status_code}).")
        return None
