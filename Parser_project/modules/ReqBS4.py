"""
Parsing product page using bs4 and requests
"""

from load_django import *
from parser_app.models import Product
import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0'
}

url = "https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html"

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')


# -------------------------
# CLEANER
# -------------------------
def clean_text(text):
    if not text:
        return None
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -------------------------
# TITLE
# -------------------------
title = None
try:
    title = clean_text(soup.find("h1").text)
except AttributeError:
    title = None


# -------------------------
# PRICE
# -------------------------
price = None
try:
    price = clean_text(soup.find("div", class_="product-price__big").text)
except AttributeError:
    price = None


# -------------------------
# SALE PRICE
# -------------------------
sale_price = None
try:
    sale_price = clean_text(soup.find("div", class_="product-price__old").text)
except AttributeError:
    sale_price = None


# -------------------------
# IMAGES
# -------------------------
images = []

for img in soup.select("img"):
    src = img.get("src")
    if src and "jpg" in src:
        if src.startswith("//"):
            src = "https:" + src
        images.append(src)


# -------------------------
# CHARACTERISTICS (FIXED + CLEANED)
# -------------------------
characteristics = {}

for block in soup.select("div.br-pr-chr-item"):
    rows = block.select("div > div")

    for row in rows:
        spans = row.find_all("span")

        if len(spans) >= 2:
            key = clean_text(spans[0].get_text())
            value = clean_text(spans[1].get_text(" "))

            characteristics[key] = value


# финальная чистка всего dict
characteristics = {
    clean_text(k): clean_text(v)
    for k, v in characteristics.items()
}


# -------------------------
# DERIVED FIELDS
# -------------------------
color = characteristics.get("Колір")
memory = characteristics.get("Вбудована пам'ять")
brand = characteristics.get("Виробник")
screen_size = characteristics.get("Діагональ екрану")
resolution = characteristics.get("Роздільна здатність екрану")


# -------------------------
# PRODUCT CODE
# -------------------------
product_code = characteristics.get("Артикул")


# -------------------------
# REVIEWS (optional fallback)
# -------------------------
reviews = None
text = soup.get_text(" ", strip=True)

match = re.search(r"(\d+)\s*відгук", text)
if match:
    reviews = int(match.group(1))


# -------------------------
# PRODUCT OBJECT
# -------------------------
product = {
    "title": title,
    "color": color,
    "memory": memory,
    "brand": brand,
    "price": price,
    "sale_price": sale_price,
    "images": images,
    "product_code": product_code,
    "reviews_count": reviews,
    "screen_size": screen_size,
    "resolution": resolution,
    "characteristics": characteristics
}


# -------------------------
# OUTPUT
# -------------------------
for key, value in product.items():
    print("=" * 50)
    print(f"{key}: {value}")


# -------------------------
# SAVE (optional)
# -------------------------
Product.objects.create(**product)