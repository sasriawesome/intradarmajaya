from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MEDIA_URL = "/media/"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2&=-1986d_nd=477i0c04)n@2nf#h@+@4*8b789y81&$z0!&pq'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

try:
    from .local import *
except ImportError:
    pass
