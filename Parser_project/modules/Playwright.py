"""
Parsing product page using playwright
"""

from load_django import *
from parser_app.models import Product

from playwright.sync_api import sync_playwright

import re
import time


def clean_text(text):
    if not text:
        return None
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_price(text):
    if not text:
        return None
    text = re.sub(r"[^\d]", "", text)
    return float(text) if text else None


product = None

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://brain.com.ua/", timeout=60000)
    page.wait_for_load_state("networkidle")

    inputs = page.query_selector_all("input[type='text']")

    search_input = None
    for inp in inputs:
        if inp.is_visible():
            search_input = inp
            break

    if not search_input:
        raise Exception("Поисковое поле не найдено")

    search_input.click()
    search_input.fill("Apple iPhone 15 128GB Black")
    search_input.press("Enter")

    page.wait_for_selector("a[href*='Mobilniy_telefon']")
    page.locator("a[href*='Mobilniy_telefon']").first.click()

    page.wait_for_selector("h1.desktop-only-title")
    time.sleep(2)

    try:
        title = clean_text(page.locator("h1.desktop-only-title").inner_text())
    except:
        title = None

    price = None
    sale_price = None

    try:
        sale_locator = page.locator(".br-pr-np span")
        if sale_locator.count() > 0:
            sale_price = parse_price(clean_text(sale_locator.first.inner_text()))
            price = parse_price(clean_text(page.locator(".br-pr-op span").first.inner_text()))
        else:
            price = parse_price(clean_text(page.locator(".br-pr-op span").first.inner_text()))
            sale_price = None
    except:
        price = None
        sale_price = None

    images = []
    img_elements = page.query_selector_all("img[src*='prod_img']")
    for img in img_elements:
        src = img.get_attribute("src")
        if src and src not in images:
            images.append(src)

    try:
        btn = page.locator(".br-prs-button")
        if btn.is_visible():
            btn.click()
            time.sleep(1)
    except:
        pass

    characteristics = {}
    sections = page.query_selector_all(".br-pr-chr-item")

    for section in sections:
        rows = section.query_selector_all("div")

        for row in rows:
            spans = row.query_selector_all("span")
            if len(spans) >= 2:
                key = clean_text(spans[0].inner_text())
                value = clean_text(spans[1].inner_text())
                if key and value:
                    characteristics[key] = value

    color = characteristics.get("Колір")
    memory = characteristics.get("Вбудована пам'ять")
    brand = characteristics.get("Виробник")
    screen_size = characteristics.get("Діагональ екрану")
    resolution = characteristics.get("Роздільна здатність екрану")
    product_code = characteristics.get("Артикул")

    reviews = 0
    try:
        el = page.locator("a.brackets-reviews")
        if el.count() > 0:
            text = el.first.inner_text()
            match = re.search(r"\((\d+)\)", text)
            if match:
                reviews = int(match.group(1))
    except:
        reviews = 0

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

    browser.close()


for key, value in product.items():
    print("=" * 50)
    print(f"{key}: {value}")

if product_code:
    Product.objects.update_or_create(
        product_code=product_code,
        defaults=product
    )
else:
    Product.objects.create(**product)

print("\n✅ Saved to DB")