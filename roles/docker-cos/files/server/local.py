import os

SECRET_KEY = 'Super#Secret!Key'

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cos_staging',
        # 'USER': 'postgres',
        # 'PASSWORD': '<blank>',
        'HOST': os.environ.get('POSTGRES_PORT_5432_TCP_ADDR', ''),
        'PORT': os.environ.get('POSTGRES_PORT_5432_TCP_PORT', ''),
    }
}
