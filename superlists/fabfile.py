import os

from fabric.api import cd, env, local, run, task, sudo
from fabric.contrib.files import append, exists, sed
from fabric.colors import green, red

env.user = 'javerbukh'
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
    # _setup_directory()
    source_folder = '/home/{}/sites/{}/source'.format(env.user, env.site_name)
    _pull(source_folder)
    with cd(source_folder):
        _make_virtualenv()
        _collectstatic()
        _db_migrate()
    # update_server_configs()
    # restart_services()
    print(red("Done!"))

@task
def update_server_configs():
    pass

@task
def restart_services():
    sudo('service nginx reload')
    # Add something for restarting gunicorn

def _setup_directory(site_folder):
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
        sudo('git reset --hard {}'.format(source_folder, current_commit))
        # The superlists directory contains the source code so we copy it here
        sudo('mv superlists tmp')
        sudo('cp tmp/* .')
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
