## Provisioning a new site
Summary of provisioning using Ubuntu, Nginx, Gunicorn, and Upstart

### Summary
* Set up folder structure with a user account and home folder
* Setup Ubuntu with our tools/packages
* Add Nginx virtual host configs
* Add Upstart job for Gunicorn

### Folder structure
Assume we have a user account at `/home/username`. Our folder directory looks like
```
/home/username
    --- sites
        --- SITENAME
             --- database
             --- source
             --- static
    --- .virtualenvs
```

### Ubuntu
First we setup the tools and packages we need
    sudo apt-get update
    sudo apt-get install nginx git python3 python3-pip
    sudo pip3 install virtualenv

### Nginx
* See nginx.template.conf
* Replace SITENAME with e.g. nezaj-lists.com

### Upstart
* See gunicorn-upstart.template.conf
* Replace SITENAME with e.g. nezaj-lists.com
