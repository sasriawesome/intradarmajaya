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

# EMAIL CONFIG
# ======================================================================

EMAIL_USE_TLS = True
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = env('EMAIL_HOST_PASSWORD')
EMAIL_HOST_PASSWORD = DEFAULT_FROM_EMAIL
EMAIL_BACKEND = env('EMAIL_BACKEND')

DEBUG = False

try:
    from .local import *
except ImportError:
    pass
