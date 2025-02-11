# method3/utils.py

def clean_price(price_str):
    """Convertit une chaîne de prix en float (ex: '£51.77' -> 51.77)."""
    return float(price_str.lstrip('£'))

def clean_stock(stock_str):
    """Extrait le nombre de livres disponibles d'une chaîne (ex: 'In stock (22 available)' -> 22)."""
    return int(''.join(filter(str.isdigit, stock_str)))

def make_absolute_url(relative_url):
    """Transforme une URL relative en URL absolue."""
    return 'https://books.toscrape.com/' + relative_url.replace('../', '')
