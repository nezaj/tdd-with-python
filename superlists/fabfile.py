import os

# Fabric is not part of virtualenv
# pylint: disable=import-error
from fabric.api import cd, env, local, task, sudo
from fabric.contrib.files import exists
from fabric.colors import green, red

env.user = 'javerbukh'
env.app_env = 'prod'
env.hosts = [os.environ.get('NZL_URL')]
env.site_name = 'nezaj-lists.com'

REPO_URL = 'https://github.com/nezaj/tdd-with-python.git'

@task
def bootstrap():
    """Sets up a new server with our tools"""
    print(green("Bootstrapping {}".format(env.host)))
    sudo('apt-get update')
    sudo('apt-get install nginx git python3 python3-pip')
    sudo('pip3 install virtualenv')

@task
def deploy():
    """Deploys current release to web server"""
    print(red("Beginning Deploy:"))
    _setup_directory()
    source_folder = '/home/{}/sites/{}/source'.format(env.user, env.site_name)
    _pull(source_folder)
    with cd(source_folder):
        _make_virtualenv()
        _collectstatic()
        _db_migrate()
    update_server_configs(source_folder)
    restart_services()
    _tag_live()
    print(red("Deploy complete!"))

@task
def update_server_configs(source_folder):
    """Updates webserver configs"""
    update_nginx_config(source_folder)
    update_gunicorn_upstart_config(source_folder)

@task
def update_nginx_config(source_folder):
    """Copies environment specific nginx configuration to sites-available and creates symlink"""
    print(green("Updating nginx configuration..."))
    source_nginx = source_folder + '/etc/nginx/{}.conf'.format(env.app_env)
    available_nginx = '/etc/nginx/sites-available/{}.conf'.format(env.site_name)
    sudo('cp {} {}'.format(source_nginx, available_nginx))

    enabled_nginx = '/etc/nginx/sites-enabled/{}.conf'.format(env.site_name)
    sudo('ln -sf {} {}'.format(available_nginx, enabled_nginx))

@task
def update_gunicorn_upstart_config(source_folder):
    """Copies environment specific gunicorn-upstart configuration to init"""
    print(green("Updating gunicorn-upstart configuration..."))
    source_upstart = source_folder + '/etc/gunicorn-upstart/{}.conf'.format(env.app_env)
    target_upstart = '/etc/init/gunicorn-{}.conf'.format(env.site_name)
    sudo('cp {} {}'.format(source_upstart, target_upstart))

@task
def restart_services():
    """Restarts nginx and gunicorn-upstart"""
    print(green("Reloading nginx and gunicorn"))
    sudo('service nginx reload')
    sudo('service gunicorn-{} reload'.format(env.site_name))

def _setup_directory():
    print(green("Creating directory structure if neccessary..."))
    site_folder = '/home/{}/sites/{}'.format(env.user, env.site_name)
    for subfolder in ('database', 'static', 'source'):
        sudo('mkdir -p {}/{}'.format(site_folder, subfolder))

def _pull(source_folder):
    print(green("Pulling master from GitHub..."))
    if exists(source_folder + '/.git'):
        sudo('cd {} && git fetch'.format(source_folder))
    else:
        sudo('git clone {} {}'.format(REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    with cd(source_folder):
        sudo('git reset --hard {}'.format(current_commit))
        # The superlists directory contains the source code so we copy it here
        if exists('tmp'):
            sudo('rm -rf tmp')
        sudo('mv superlists tmp')
        sudo('cp -R tmp/* .')
        sudo('rm -rf tmp')

def _make_virtualenv():
    print(green("Installing requirements..."))
    sudo('make virtualenv')

def _collectstatic():
    print(green("Collecting static files..."))
    sudo('make collectstatic')

def _db_migrate():
    print(green("Migrating the database..."))
    sudo('make db-migrate')

def _tag_live():
    print(green("Updating LIVE tag..."))
    local('git tag -f LIVE')
    local('git push -f origin LIVE')
