from .base import *

USE_X_FORWARDED_HOST = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_TRUSTED_ORIGINS = [
    'intra.darmajaya.ac.id',
    'intradarmajaya.herokuapp.com',
    'intradarmajaya-nginx.herokuapp.com',
]

MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEBUG = False

try:
    from .local import *
except ImportError:
    pass
