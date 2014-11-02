"""
Settings for each enviornment is defined in a separate module.
To use a different enviornment set the APP_ENV variable.

Default enviornment is dev
"""
import os

env_to_module = {
    'dev': 'settings.dev',
    'stage': 'setting.stage',
    'prod': 'settings.prod',

    'default': 'settings.dev'
}

app_config = env_to_module[os.getenv('APP_ENV', 'default')]
