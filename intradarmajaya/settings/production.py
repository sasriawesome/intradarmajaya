from .base import *

DEBUG = env.bool("DEBUG", True)

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = [
    'www.darmajaya.net',
    'intra.darmajaya.ac.id',
    '*.apps.simpellab.com',
]

# EMAIL CONFIG
# ======================================================================

# EMAIL WEB API
EMAIL_USE_TLS = True
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = env('EMAIL_HOST_PASSWORD')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# CDN
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_DEFAULT_ACL = 'public-read'
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL')
AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')
AWS_LOCATION = env('AWS_LOCATION')

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

try:
    from .local import *
except ImportError:
    pass
