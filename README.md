# Parser Project

A Django-based web scraping project built to practice and compare three approaches to data extraction:

* `Requests + BeautifulSoup`
* `Selenium`
* `Playwright`

The project is designed to help understand how each library works, how to use it for basic scraping tasks, and how to extract product data from a real e-commerce website.

## Goal

The main goal of this project is to learn and practice the following libraries at a basic working level:

* **Requests** — sending HTTP requests and receiving HTML pages.
* **BeautifulSoup (BS4)** — parsing HTML and extracting data from the DOM.
* **XPath** — selecting elements manually for Selenium and Playwright.
* **Selenium** — browser automation and scraping dynamic pages.
* **Playwright** — modern browser automation and scraping dynamic pages.

The project is intended as preparation for internship tasks and basic real-world scraping assignments.

## What the project includes

The project contains three parsers:

1. **Requests / BeautifulSoup parser**
2. **Selenium parser**
3. **Playwright parser**

Each parser follows the same general idea:

* open a product page or product listing
* extract product information
* normalize the data
* save the result to PostgreSQL through Django models

## Main features

* Product title parsing
* Price and sale price parsing
* Image links collection
* Product code extraction
* Review count extraction
* Product characteristics extraction as a dictionary
* Saving parsed data into PostgreSQL

## Technologies used

* Python
* Django
* PostgreSQL
* Requests
* BeautifulSoup4
* Selenium
* Playwright
* XPath
* webdriver-manager

## Project structure

```text
Parser_project/
├── modules/
│   ├── load_django.py
│   ├── Playwright.py
│   ├── ReqBS4.py
│   ├── SeleniumParserScript.py
│   └── status.py
├── Parser_project/
│   ├── parser_app/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── Parser_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   └── manage.py
├── results/
├── requirements.txt
└── README.md
```

## Requirements

Create and activate a virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

For Playwright, install browsers separately:

```bash
playwright install
```

## How to run

Run the parser script from the `modules` folder or from your configured environment.

Examples:

```bash
python modules/ReqBS4.py
python modules/SeleniumParserScript.py
python modules/Playwright.py
```

Make sure the Django environment is loaded correctly before saving data to the database.

## Important assignment notes

This project was created according to the assignment requirements:

* Study each library at a level sufficient for basic practical use.
* Build three parsers using different approaches.
* Select classes and XPath manually.
* Do not copy ready-made selectors from other sources.
* Use XPath in Selenium and Playwright.
* Use manual class selection in BeautifulSoup.

## Data model

The project stores parsed products in a Django model backed by PostgreSQL.
The model includes fields such as:

* title
* brand
* color
* memory
* screen size
* resolution
* price
* sale price
* product code
* review count
* images
* characteristics

## Notes

* `characteristics` is stored as a dictionary-like JSON field.
* `images` is stored as a list-like JSON field.
* Product records are updated by `product_code` when it is available.
* The project is structured to support further expansion and experimentation with new parsing strategies.

## Learning outcome

By working with this project, you should be able to:

* understand how Requests, BeautifulSoup, Selenium, and Playwright differ
* extract data from static and dynamic websites
* select HTML elements manually
* handle common scraping problems
* save parsed data into a database

## License

This project is intended for educational use.
