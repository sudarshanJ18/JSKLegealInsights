import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")  # Ensure it's set in .env
DEBUG = os.getenv("DEBUG", "False").lower() == "true"  # Properly convert string to boolean

# ALLOWED_HOSTS configuration
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'JSKLegalInsightsapp',
    'django_summernote',
    'whitenoise.runserver_nostatic',  # For better static file serving
    'algoliasearch_django',
    'rest_framework',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'JSKLegalInsights.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'JSKLegalInsightsapp' / 'templates'],
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

WSGI_APPLICATION = 'JSKLegalInsights.wsgi.application'

# Database configuration - PostgreSQL for production
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,  # Keep connections alive for 10 minutes
        ssl_require=True,  # Require SSL for secure connections
    )
}

CRON_CLASSES = [
    "JSKLegalInsightsapp.cron.FetchLegalDataCronJob",
]

# Authentication
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static & Media Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / "JSKLegalInsightsapp/static"]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# Whitenoise for static file compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default Primary Key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# Logging for production
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "django_errors.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}

# API Keys and External Services
API_KEY = os.getenv("INDIAN_KANOON_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWSDATA_API_KEY = os.getenv("NEWS_API_KEY")

# Algolia Search Configuration
ALGOLIA = {
    'APPLICATION_ID': os.getenv('ALGOLIA_APPLICATION_ID'),
    'API_KEY': os.getenv('ALGOLIA_API_KEY'),
    'INDEX_NAME': os.getenv('ALGOLIA_INDEX_NAME'),
}