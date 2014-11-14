MAKEFLAGS = --no-print-directory --always-make --silent
MAKE = make $(MAKEFLAGS)

# Use python3 for this project
PY3_PATH = /usr/local/bin/python3
VENVFLAGS = --python=$(PY3_PATH)
VIRTUALENV = virtualenv $(VENVFLAGS)

# Follow convention of creating virtualenvs in ~/.virtualenvs
VENV_NAME = superlists
VENV_PATH = ~/.virtualenvs/$(VENV_NAME)
VENV_ACTIVATE = . $(VENV_PATH)/bin/activate

# Don't analyze library/minified Javascript
JS_ROOT = lists/static/
JS_FILES = $(shell find $(JS_ROOT) -name '*.js' \
             -not -path '$(JS_ROOT)/bootstrap/*.js' \
             -not -name 'qunit.js' \
             -not -name '*.min.js')

clean:
	find . -name "*.pyc" -print -delete
	rm -rfv $(VENV_PATH)

check:
	$(MAKE) virtualenv
	$(MAKE) pylint pep8 test

virtualenv:
	test -d $(VENV_PATH) || $(VIRTUALENV) $(VENV_PATH)
	$(VENV_ACTIVATE) && pip install -r requirements.txt
	rm -rf superlists.egg-info

pep8:
	@echo "Running pep8..."
	$(VENV_ACTIVATE) && \
	pep8 lists && \
	pep8 superlists && \
	pep8 *.py

pylint:
	@echo "Running pylint..."
	$(VENV_ACTIVATE) && \
	pylint lists && \
	pylint superlists && \
	pylint *.py

jshint:
	@echo "Running JSHint..."
	jshint $(JS_FILES)

test:
	@echo "Running all django tests..."
	$(VENV_ACTIVATE) && ./manage.py test

unit-test:
	@echo "Running all unit tests..."
	$(VENV_ACTIVATE) && ./manage.py test lists

func-test:
	@echo "Running all functional tests..."
	$(VENV_ACTIVATE) && ./manage.py test functional_tests

live-test:
	@echo "Running all functional tests..."
	$(VENV_ACTIVATE) && ./manage.py test functional_tests --liveserver=nezaj-lists.com

rev:
	@echo "Generating new migration file..."
	$(VENV_ACTIVATE) && ./manage.py makemigrations

collectstatic:
	@echo "Collecting static files..."
	$(VENV_ACTIVATE) && ./manage.py collectstatic --noinput

db-migrate:
	@echo "Upgrading database to head revision..."
	$(VENV_ACTIVATE) && ./manage.py migrate --noinput
