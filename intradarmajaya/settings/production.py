from .base import *

DEBUG = True

BASE_URL = 'http://intra.darmajaya.ac.id'



# HEROKU SETUP
# ============================================================

# Change 'default' database configuration with $DATABASE_URL.
DATABASES['default'].update(dj_database_url.config(conn_max_age=500, ssl_require=True))

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Activate Django-Heroku.
django_heroku.settings(locals())

try:
    from .local import *
except ImportError:
    pass
