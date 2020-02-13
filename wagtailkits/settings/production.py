from .base import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

INSTALLED_APPS = installed_app_base

MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

try:
    from .local import *
except ImportError:
    pass
