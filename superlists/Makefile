MAKEFLAGS = --no-print-directory --always-make --silent
MAKE = make $(MAKEFLAGS)

# We're using python3 for this project
PY3_PATH = /usr/local/bin/python3
VENVFLAGS = --python=$(PY3_PATH)
VIRTUALENV = virtualenv $(VENVFLAGS)

VENV_NAME = superlists
VENV_PATH = ~/.virtualenvs/$(VENV_NAME)
VENV_ACTIVATE = . $(VENV_PATH)/bin/activate

clean:
	find . -name "*.pyc" -print -delete
	rm -rfv $(VENV_PATH)

check:
	$(MAKE) virtualenv
	$(MAKE) pylint pep8 test

virtualenv:
	test -d $(VENV_PATH) || $(VIRTUALENV) $(VENV_PATH)
	$(VENV_ACTIVATE) && python setup.py --quiet develop
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

test:
	@echo "Django tests..."
	$(VENV_ACTIVATE) && ./manage.py test