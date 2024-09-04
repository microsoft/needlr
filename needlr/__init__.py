__version__ = "0.1.0-alpha"
from .client import FabricClient

import logging

logging.getLogger('needler').addHandler(logging.NullHandler())
