import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_KEY = '-uh7xo(=5e(@wh%9ugm!)n4ndh4cdm04ws=uzx$moj^zhazv6%'  # USE YOUR KEY
DEBUG = True
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))


# Application definition
# Add you applications here
INSTALLED_APPS = [
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Use MySql
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}
'''