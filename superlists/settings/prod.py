import os
import base64

from .base import *

# We def don't want this in prod
DEBUG = False

# Generates random 28 byte string
SECRET_KEY = base64.b4encode(os.urandom(28)).decode('utf-8')

# Used in nginx and upstart scripts
SITENAME = 'nezaj-lists.com'
