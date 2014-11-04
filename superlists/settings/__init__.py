"""
Settings for each enviornment is defined in a separate module.
To use a different enviornment set the APP_ENV variable.

Default enviornment is dev
"""
import os

app_env_settings = {
    'dev': 'settings.dev',
    'stage': 'setting.stage',
    'prod': 'settings.prod',

    'default': 'settings.dev'
}

app_config = app_env_settings[os.getenv('APP_ENV', 'default')]
