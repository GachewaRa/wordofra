"""
Django settings for wordofra project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
import os
import base64

import cloudinary
import cloudinary.uploader
import cloudinary.api


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "wordofra.onrender.com",
    "localhost",
    "127.0.0.1"
]



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'blog',
    'portfolio',
    'accounts',
    'django_extensions',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework_simplejwt',
    'djoser',
    'corsheaders',
    'cloudinary',
    'cloudinary_storage',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Add this line
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'wordofra.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'wordofra.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# settings.py

# Load environment variables from .env file
# load_dotenv()
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'my_portfolio_db',  # Your PostgreSQL database name
#         'USER': os.getenv('DB_USERNAME'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),  # Your PostgreSQL user password
#         'HOST': 'localhost',
#         'PORT': '5432',  # Default port for PostgreSQL
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
        'OPTIONS': {
            'sslmode': os.getenv('DATABASE_SSL_MODE', 'require'),
            'sslrootcert': os.path.join(BASE_DIR, os.getenv('DATABASE_CA_CERT')),
        },
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'accounts.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'home'  
LOGOUT_REDIRECT_URL = 'logout'  

AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailOrUsernameModelBackend',  # Add your custom backend here
    'django.contrib.auth.backends.ModelBackend',      # Keep Django's default backend as a fallback
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



# This is the key part - create a directory to hold media files that will be treated as static
WHITENOISE_ROOT = os.path.join(BASE_DIR, 'staticfiles', 'media')

# Keep your existing media settings
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Optional: Define MEDIA_URL if you want
MEDIA_URL = f"https://res.cloudinary.com/dyr0ityfq/"


CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv('CLOUD_NAME'),
    "API_KEY": os.getenv('CLOUDINARY_API_KEY'),
    "API_SECRET": os.getenv('CLOUDINARY_API_SECRET'),
}

cloudinary.config( 
  cloud_name = os.getenv("CLOUD_NAME"),  
  api_key = os.getenv("CLOUDINARY_API_KEY"),  
  api_secret = os.getenv("CLOUDINARY_API_SECRET")  
)


TINYMCE_DEFAULT_CONFIG = {
    "height": "500px",
    "width": "auto",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview hr anchor pagebreak",
    "toolbar": "undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image",
    "content_css": "/static/css/tinymce.css",  # Optional, add your own styles here
}


REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '45/minute',            # Limit anonymous users to 5 requests per minute
        'user': '50/minute',           # Limit authenticated users to 20 requests per minute
        'login_attempts': '5/hour',    # Specific limit for login endpoints (will need custom throttle class)
    },
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': False,
    'SERIALIZERS': {
        'user_create': 'accounts.serializers.CustomUserSerializer',
        'user': 'accounts.serializers.CustomUserSerializer',
        'current_user': 'accounts.serializers.CustomUserSerializer',
    },
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    "SEND_CONFIRMATION_EMAIL": True,
    "TOKEN_MODEL": None,
}

import sys

# Disable throttling when running tests
if 'test' in sys.argv:
    REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
        'anon': None,
        'user': None,
        'login_attempts': None,  # Disable custom login rate limit
    }


CORS_ALLOWED_ORIGINS = [
    "https://wordofra.vercel.app",  # Your Vercel domain
    "https://www.wordofra.com",     # Your new custom domain
]

# If you need to allow credentials
CORS_ALLOW_CREDENTIALS = True

# CORS_ALLOW_HEADERS = [
#     "content-type",
#     "authorization",
# ]

# CORS_EXPOSE_HEADERS = ["Content-Disposition"]


# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.yourmail.com"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = "your@email.com"
# EMAIL_HOST_PASSWORD = "yourpassword"
# DEFAULT_FROM_EMAIL = "noreply@yourdomain.com"
