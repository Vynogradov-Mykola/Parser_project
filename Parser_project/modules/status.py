import sys
import os
import django

sys.path.append('/Parser_project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'Parser_project.settings'
django.setup()