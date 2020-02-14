from .base import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

INSTALLED_APPS = installed_app_base

MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://intra.darmajaya.ac.id'

# HEROKU SETUP
# ============================================================

# Change 'default' database configuration with $DATABASE_URL.
DATABASES['default'].update(dj_database_url.config(conn_max_age=500, ssl_require=True))

try:
    from .local import *
except ImportError:
    pass
