import os
import sys
import django

# путь до папки, где лежит manage.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DJANGO_DIR = os.path.join(BASE_DIR, "Parser_project")

sys.path.append(DJANGO_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Parser_project.settings")

django.setup()