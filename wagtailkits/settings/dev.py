from .base import *

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(*1#c*+)m3bt@o4dfcr_sp63^@b4prr(59ebe$ibz+kz%o7dsk'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 


INSTALLED_APPS = [
    # 'debug_toolbar',
    'django_extensions'
] + installed_app_base

try:
    from .local import *
except ImportError:
    pass
