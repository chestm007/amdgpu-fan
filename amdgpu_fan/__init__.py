import logging
import os
import sys

LOGGER = logging.getLogger(__name__)
DEBUG = bool(os.environ.get('DEBUG', False))

logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG if DEBUG else logging.INFO,
                    format='%(message)s')
