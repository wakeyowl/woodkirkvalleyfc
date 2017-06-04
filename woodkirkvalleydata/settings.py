"""
Django settings for woodkirkvalleydata project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'templates/member/../member/static')
MEDIA_DIR = os.path.join(BASE_DIR, 'member/media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6sj+pwb&x-*sqntyhjt18#90@dwa3tket$8m6hpgq6u-1%c1&5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['wvfc.pythonanywhere.com', '127.0.0.1', 'wvfcskills.pythonanywhere.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'member',
    'registration',
    'bootstrap3',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'woodkirkvalleydata.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'woodkirkvalleydata.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # The following settings are not used with sqlite3:
        'NAME': 'wvfc$reg',
        'USER': 'wvfc',
        'PASSWORD': 'v0n-neumann',
        'HOST': 'wvfc.mysql.pythonanywhere-services.com',
        # Empty for localhost through domain sockets or   '127.0.0.1' for localhost through TCP.
        'PORT': '',
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
            'sql_mode': 'traditional',
        }
    }
    # # ,
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     # The following settings are not used with sqlite3:
    #     'NAME': 'registrations',
    #     'USER': 'root',
    #     'PASSWORD': 'v0n-neumann',
    #     'HOST': '',  # Empty for localhost through domain sockets or   '127.0.0.1' for localhost through TCP.
    #     'PORT': '',
    #     'OPTIONS': {
    #         "init_command": "SET foreign_key_checks = 0;",
    #         'sql_mode': 'traditional',
    #     }
    # }

}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_INPUT_FORMATS = ('%dd-%mm-%YYYY')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = "/home/wvfc/woodkirkvalleydata/static"
STATIC_URL = '/static/'

REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
LOGIN_REDIRECT_URL = '/member/'
LOGIN_URL = '/accounts/login/'

MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'
