"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)7$g++5jav%l_1uvd_n2g#kp!ne9tve$v62%b8)i(9f7-^ypx('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_jalali',
    'easy_thumbnails',
    'filer',
    'mptt',
    'taggit',
    'tinymce',
    'core.apps.CoreConfig',
    'accounts.apps.AccountsConfig',
    'homepage.apps.HomepageConfig',
    'products.apps.ProductsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates/',],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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


# Substituting a custom User model
# https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#substituting-a-custom-user-model

AUTH_USER_MODEL = 'accounts.User'


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fa'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [BASE_DIR / 'locale/',]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static/',]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Production database

if os.getenv('DEBUG') == 'false':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASS'),
        }
    }

# django-tinymce
# https://django-tinymce.readthedocs.io/en/latest/installation.html#configuration

TINYMCE_DEFAULT_CONFIG = {
    'menubar': 'file edit view insert format tools help',
    'plugins': 'accordion, advlist, anchor, autolink, autoresize, autosave, charmap, code, codesample, directionality, emoticons, fullscreen, help, image, link, lists, preview, quickbars, searchreplace, visualblocks, visualchars, wordcount',
    'menu': {
        'file': {'title': 'File', 'items': 'restoredefault preview'},
        'edit': {'title': 'Edit', 'items': 'undo redo | cut copy paste | selectall searchreplace'},
        'view': {'title': 'View', 'items': 'code visualaid visualblocks visualchars fullscreen'},
        'insert': {'title': 'Insert', 'items': 'image link anchor codesample charmap emoticons hr accordion'},
        'format': {'title': 'Format', 'items': 'bold italic underline strikethrough superscript subscript | blockquote | align | removeformat | rtl ltr'},
        'tools': {'title': 'Tools', 'items': 'code wordcount'},
        'help': {'title': 'Help', 'items': 'help'},
    },
    'toolbar': 'undo redo | formatselect | bold italic underline strikethrough | alignleft aligncenter alignright alignjustify | ltr rtl | bullist numlist | link image charmap emoticons | codesample code preview fullscreen | searchreplace',
    'toolbar_mode': 'sliding',
    'width': '80%',
    'min_height': 500,
    'autoresize_bottom_margin': 50,
}