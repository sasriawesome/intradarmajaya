from .base import *

DEBUG = False

BASE_URL = 'http://intra.darmajaya.ac.id'


try:
    from .local import *
except ImportError:
    pass
