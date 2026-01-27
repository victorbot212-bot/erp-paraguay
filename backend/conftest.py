"""Pytest configuration for Django."""
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

def pytest_configure():
    settings.DEBUG = True
    django.setup()
