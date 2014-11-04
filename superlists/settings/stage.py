import os
import base64

from .base import *

# We don't want this in stage
DEBUG = False

# Generates random 28 byte string
SECRET_KEY = base64.b4encode(os.urandom(28)).decode('utf-8')

# Used in nginx and upstart scripts
SITENAME = 'stage.nezaj-lists.com'
