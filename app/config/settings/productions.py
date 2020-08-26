from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ['DB_DEPLOY_HOST'],
        'NAME': os.environ['DB_DEPLOY_NAME'],
        'USER': os.environ['DB_DEPLOY_USER'],
        'PASSWORD': os.environ['DB_DEPLOY_PASSWORD'],
        'PORT': os.environ['DB_DEPLOY_PORT'],
    }
}

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware', ]