from load_django import *
from parser_app.models import Product

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

import time
import re


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
# PARSE PRICE
# -------------------------
def parse_price(text):
    if not text:
        return None
    text = re.sub(r"[^\d]", "", text)
    return float(text) if text else None


# -------------------------
# DRIVER
# -------------------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 15)

driver.get("https://brain.com.ua/")

wait = WebDriverWait(driver, 20)

# Ждем ВСЕ input поиска
inputs = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']"))
)

search_input = None

# Берем только ВИДИМЫЙ
for inp in inputs:
    if inp.is_displayed():
        search_input = inp
        break

if not search_input:
    raise Exception("Поисковое поле не найдено")

# Кликаем и вводим
search_input.click()
search_input.clear()
search_input.send_keys("Apple iPhone 15 128GB Black")

# -------------------------
# STEP 4: OPEN FIRST PRODUCT
# -------------------------
first_product = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "(//a[contains(@href, 'Mobilniy_telefon')])[1]")
    )
)

first_product.click()

# -------------------------
# WAIT PRODUCT PAGE
# -------------------------
wait.until(EC.presence_of_element_located((By.XPATH, "//h1")))
time.sleep(2)

# -------------------------
# TITLE
# -------------------------
try:
    title = clean_text(
        driver.find_element(By.XPATH, "//h1[contains(@class,'desktop-only-title')]").text
    )
except:
    title = None

# -------------------------
# PRICE
# -------------------------
try:
    price = clean_text(
        driver.find_element(By.XPATH, "//div[contains(@class,'br-pr-op')]//span").text
    )
    price = parse_price(price)
except:
    price = None

# -------------------------
# SALE PRICE
# -------------------------
try:
    sale_price = clean_text(
        driver.find_element(By.XPATH, "//div[contains(@class,'br-pr-np')]//span").text
    )
    sale_price = parse_price(sale_price)
except:
    sale_price = None

# -------------------------
# IMAGES
# -------------------------
images = []
img_elements = driver.find_elements(By.XPATH, "//img[contains(@src, 'prod_img')]")

for img in img_elements:
    src = img.get_attribute("src")
    if src and src not in images:
        images.append(src)
try:
    btn = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "br-prs-button"))
    )
    btn.click()
except:
    pass
# -------------------------
# CHARACTERISTICS
# -------------------------
print(len(driver.find_elements(By.CLASS_NAME, "br-pr-chr-item")))
characteristics = {}

sections = driver.find_elements(By.CSS_SELECTOR, ".br-pr-chr-item")

for section in sections:
    rows = section.find_elements(By.XPATH, ".//div[span[1] and span[2]]")

    for row in rows:
        key = row.find_element(By.XPATH, "./span[1]").get_attribute("textContent")
        value = row.find_element(By.XPATH, "./span[2]").get_attribute("textContent")

        key = clean_text(key)
        value = clean_text(value)

        if key and value:
            characteristics[key] = value

# -------------------------
# DERIVED
# -------------------------
color = characteristics.get("Колір")
memory = characteristics.get("Вбудована пам'ять")
brand = characteristics.get("Виробник")
screen_size = characteristics.get("Діагональ екрану")
resolution = characteristics.get("Роздільна здатність екрану")

product_code = characteristics.get("Артикул")

# -------------------------
# REVIEWS
# -------------------------
reviews = None

try:
    el = driver.find_element(By.CSS_SELECTOR, "a.brackets-reviews")

    text = el.text  # "Відгуки (9)"

    match = re.search(r"\((\d+)\)", text)
    if match:
        reviews = int(match.group(1))

except:
    reviews = 0
# -------------------------
# FINAL OBJECT
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
# SAVE TO DB
# -------------------------
if product_code:
    Product.objects.update_or_create(
        product_code=product_code,
        defaults=product
    )
else:
    Product.objects.create(**product)

print("\n✅ Saved to DB")

driver.quit()
