#!/usr/bin/env python3
import os
import sys

from settings import app_config

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", app_config)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
