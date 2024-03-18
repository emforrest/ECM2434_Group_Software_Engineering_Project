from .base import *
import os

if os.environ.get('DJANGO_LOGGING') != 'False':
    from .logging import *

# Load the correct config according to the type of environment config
if os.environ.get("DJANGO_ENV") == 'production':
    from .production import *
else:
    from .local import *