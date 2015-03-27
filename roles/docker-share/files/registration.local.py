import os

SECRET_KEY = 'Secret!Key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'share_registration',
        # 'USER': 'postgres',
        # 'PASSWORD': '<blank>',
        'HOST': os.environ.get('POSTGRES_PORT_5432_TCP_ADDR', ''),
        'PORT': os.environ.get('POSTGRES_PORT_5432_TCP_PORT', ''),
    }
}
