## Deploying a new site
Summary of deploying process after our server has been provisioned

### Summary
* Create directory structure in ~/sites
* Pull down source code into folder named source
* `make virtualenv` and activate
* manage.py migrate for database
* collectstatic for static files
* Set DEBUG = False and ALLOWED_HOSTS in settings.py
* Restart Gunicorn job
* Run FTs to check everything works
