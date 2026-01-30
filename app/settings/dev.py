"""
Django development settings for app project.

Settings for local development environment.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database - SQLite for development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Email backend for development (prints to console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Django Debug Toolbar
INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# Debug Toolbar settings
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
}
