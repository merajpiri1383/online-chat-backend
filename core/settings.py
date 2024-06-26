import os

from charset_normalizer import CharsetMatches
# config for .env file
from dotenv import load_dotenv
from datetime import timedelta
load_dotenv()

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4-pvw!9*sa8a%6ynfcf#cg(363tp=bo%crex$@l1b!$(vxx-qv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG",True)

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS","127.0.0.1,localhost").split(",")

# custom user model
AUTH_USER_MODEL = "user.User"

# Application definition

INSTALLED_APPS = [
    # external apps
    'channels',
    'rest_framework',
    'drf_spectacular',
    'rest_framework_simplejwt',
    'corsheaders',
    
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # internal apps
    'user.apps.UserConfig',
    'chat.apps.ChatConfig',
    'account.apps.AccountConfig',
    'group.apps.GroupConfig',
    'profuser.apps.ProfuserConfig',
    'channel.apps.ChannelConfig',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# cors headers settings

CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS","http://127.0.0.1:3000,http://localhost:3000").split(",")

# channel layers 


ASGI_APPLICATION = "core.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}


# rest framework settings
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS" : "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES" : [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ]
}

# drf spectacular settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'online-chat',
    'DESCRIPTION': 'backend of online chat build with django rest framework',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# jwt authentication settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME" : timedelta(minutes=20),
    "REFRESH_TOKEN_LIFETIME" : timedelta(days=3)
}

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# celery settings
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL','amqp://guest@localhost:5672/')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND','redis://localhost:6379/')

# media configuration
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR /"media"

# sms.ir
SMS_API_KEY = os.getenv("SMS_API_KEY")
SMS_LINE_NUMBER = os.getenv("SMS_LINE_NUMBER")

# caching
CACHES = {
    "default": {
        "BACKEND" : "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION" : "127.0.0.1:11211",
    }
}

USER_ONLINE_TIMEOUT = 300
USER_LASTSEEN_TIMEOUT = 60 * 60 * 24 * 7