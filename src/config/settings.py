# src/config/settings.py

import os
from pathlib import Path
import environ
from django.utils.translation import gettext_lazy as _

# --- Environment Setup ---
env = environ.Env(
    DEBUG=(bool, False)
)

# --- Path Configuration ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Core Django Settings ---
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# --- Application Definition ---

# This is the single, correctly ordered list of installed apps.
# Third-party apps that modify the admin must come BEFORE 'django.contrib.admin'.
INSTALLED_APPS = [
    # Core Django apps (admin is moved down)
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    # Third-party apps
    'rest_framework', # <--- ADDED DRF
    'corsheaders', # <--- ADDED CORSHEADERS
    'import_export',
    'mptt',
    'modeltranslation',
    'solo',
    
    # Then the admin itself
    'django.contrib.admin',

    # And finally our local apps
    'core.apps.CoreConfig',
    'accounts.apps.AccountsConfig',
    'locations.apps.LocationsConfig',
    'categories.apps.CategoriesConfig',
    'listings.apps.ListingsConfig',
    'reviews.apps.ReviewsConfig',
    'notifications.apps.NotificationsConfig',
    'content.apps.ContentConfig',
    'news.apps.NewsConfig',
    'places.apps.PlacesConfig',
    'payments.apps.PaymentsConfig',
    'subscriptions.apps.SubscriptionsConfig',
    'advertising.apps.AdvertisingConfig',
    'search.apps.SearchConfig',
    'analytics.apps.AnalyticsConfig',
    'moderation.apps.ModerationConfig',
    'security.apps.SecurityConfig',
    'currencies.apps.CurrenciesConfig',
    'chat.apps.ChatConfig',
    'settings.apps.SettingsConfig',
    'api.apps.ApiConfig', # <--- ADDED OUR NEW API APP
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # <--- ADDED CORSHEADERS MIDDLEWARE
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# --- Database Configuration ---
DATABASES = {
    'default': env.db_url('DATABASE_URL', engine='django.contrib.gis.db.backends.postgis')
}

# --- Password Validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization ---
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
)
gettext = lambda s: s
LANGUAGES_MODELTRANSLATION = gettext
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Static Files (CSS, JavaScript, Images) ---
STATIC_URL = 'static/'

# --- Default primary key field type ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Custom User Model ---
AUTH_USER_MODEL = 'accounts.CustomUser'

# --- Media Files Configuration ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'