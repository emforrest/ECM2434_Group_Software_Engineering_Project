from .base import *
from .logging import *
import os

# Load the correct config according to the type of environment config
if os.environ.get("DJANGO_ENV") == 'production':
    from .production import *
else:
    from .local import *