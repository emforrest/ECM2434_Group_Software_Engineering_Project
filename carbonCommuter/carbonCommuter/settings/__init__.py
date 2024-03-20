"""Django Settings Module

Configures the settings based on the the value of the DJANGO_ENV environment variable

Authors:
- Sam Townley
"""

from .base import *
import os

# Disable logging if there is a flag set to false in the environment config
if os.environ.get('DJANGO_LOGGING') != 'False':
    from .logging import *

# Load the correct config according to the type of environment config
if os.environ.get("DJANGO_ENV") == 'production':
    from .production import *
else:
    from .local import *