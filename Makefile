# Project settings
PROJECT := TemplateDemo
PACKAGE := demo
REPOSITORY := jacebrowning/template-python-demo
PACKAGES := $(PACKAGE) tests
CONFIG := $(shell ls *.py)
MODULES := $(shell find $(PACKAGES) -name '*.py') $(CONFIG)

# Python settings
ifndef TRAVIS
	PYTHON_MAJOR ?= 2
	PYTHON_MINOR ?= 7
endif

# System paths
PLATFORM := $(shell python -c 'import sys; print(sys.platform)')
ifneq ($(findstring win32, $(PLATFORM)), )
	WINDOWS := true
	SYS_PYTHON_DIR := C:\\Python$(PYTHON_MAJOR)$(PYTHON_MINOR)
	SYS_PYTHON := $(SYS_PYTHON_DIR)\\python.exe
	SYS_VIRTUALENV := $(SYS_PYTHON_DIR)\\Scripts\\virtualenv.exe
	# https://bugs.launchpad.net/virtualenv/+bug/449537
	export TCL_LIBRARY=$(SYS_PYTHON_DIR)\\tcl\\tcl8.5
else
	ifneq ($(findstring darwin, $(PLATFORM)), )
		MAC := true
	else
		LINUX := true
	endif
	SYS_PYTHON := python$(PYTHON_MAJOR)
	ifdef PYTHON_MINOR
		SYS_PYTHON := $(SYS_PYTHON).$(PYTHON_MINOR)
	endif
	SYS_VIRTUALENV := virtualenv
endif

# Virtual environment paths
ENV := env
ifneq ($(findstring win32, $(PLATFORM)), )
	BIN := $(ENV)/Scripts
	ACTIVATE := $(BIN)/activate.bat
	OPEN := cmd /c start
else
	BIN := $(ENV)/bin
	ACTIVATE := . $(BIN)/activate
	ifneq ($(findstring cygwin, $(PLATFORM)), )
		OPEN := cygstart
	else
		OPEN := open
	endif
endif

# Virtual environment executables
ifndef TRAVIS
	BIN_ := $(BIN)/
endif
PYTHON := $(BIN_)python
PIP := $(BIN_)pip
EASY_INSTALL := $(BIN_)easy_install
RST2HTML := $(PYTHON) $(BIN_)rst2html.py
PDOC := $(PYTHON) $(BIN_)pdoc
MKDOCS := $(BIN_)mkdocs
PEP8 := $(BIN_)pep8
PEP8RADIUS := $(BIN_)pep8radius
PEP257 := $(BIN_)pep257
PYLINT := $(BIN_)pylint
PYREVERSE := $(BIN_)pyreverse
NOSE := $(BIN_)nosetests
PYTEST := $(BIN_)py.test
COVERAGE := $(BIN_)coverage
COVERAGE_SPACE := $(BIN_)coverage.space
SNIFFER := $(BIN_)sniffer
HONCHO := PYTHONPATH=$(PWD) $(ACTIVATE) && $(BIN_)honcho

# MAIN TASKS ###################################################################

.PHONY: all
all: doc

.PHONY: ci
ci: check test ## Run all tasks that determine CI status

.PHONY: watch
watch: depends .clean-test ## Continuously run all CI tasks when files chanage
	$(SNIFFER)

# SYSTEM DEPENDENCIES ##########################################################

.PHONY: doctor
doctor:  ## Confirm system dependencies are available
	@ echo "Checking Python version:"
	@ python --version | tee /dev/stderr | grep -q "2.7."

# PROJECT DEPENDENCIES #########################################################

DEPENDS := $(ENV)/.depends
DEPENDS_CI := $(ENV)/.depends-ci
DEPENDS_DEV := $(ENV)/.depends-dev

env: $(PYTHON)

$(PYTHON):
	$(SYS_VIRTUALENV) --python $(SYS_PYTHON) $(ENV)
	$(PYTHON) -m pip install --upgrade pip setuptools

.PHONY: depends
depends: env $(DEPENDS) $(DEPENDS_CI) $(DEPENDS_DEV) ## Install all project dependencies

$(DEPENDS): setup.py requirements.txt
	$(PYTHON) setup.py develop
	@ touch $@  # flag to indicate dependencies are installed

$(DEPENDS_CI): requirements/ci.txt
	$(PIP) install --upgrade -r $^
	@ touch $@  # flag to indicate dependencies are installed

$(DEPENDS_DEV): requirements/dev.txt
	$(PIP) install --upgrade -r $^
ifdef WINDOWS
	@ echo "Manually install pywin32: https://sourceforge.net/projects/pywin32/files/pywin32"
else ifdef MAC
	$(PIP) install --upgrade pync MacFSEvents
else ifdef LINUX
	$(PIP) install --upgrade pyinotify
endif
	@ touch $@  # flag to indicate dependencies are installed

# CHECKS #######################################################################

.PHONY: check
check: pep8 pep257 pylint ## Run linters and static analysis

.PHONY: pep8
pep8: depends ## Check for convention issues
	$(PEP8) $(PACKAGES) $(CONFIG) --config=.pep8rc

.PHONY: pep257
pep257: depends ## Check for docstring issues
	$(PEP257) $(PACKAGES) $(CONFIG)

.PHONY: pylint
pylint: depends ## Check for code issues
	$(PYLINT) $(PACKAGES) $(CONFIG) --rcfile=.pylintrc

.PHONY: fix
fix: depends
	$(PEP8RADIUS) --docformatter --in-place

# TESTS ########################################################################

RANDOM_SEED ?= $(shell date +%s)

NOSE_OPTS := --with-doctest --with-cov --cov=$(PACKAGE) --cov-report=html  --cov-report=term-missing

.PHONY: test
test: test-all ## Run unit and integration tests

.PHONY: test-unit
test-unit: depends .clean-test ## Run the unit tests
	$(NOSE) $(PACKAGE) $(NOSE_OPTS)
ifndef TRAVIS
ifndef APPVEYOR
	$(COVERAGE_SPACE) $(REPOSITORY) unit
endif
endif

.PHONY: test-int
test-int: depends .clean-test ## Run the integration tests
	$(NOSE) tests $(NOSE_OPTS)
ifndef TRAVIS
ifndef APPVEYOR
	$(COVERAGE_SPACE) $(REPOSITORY) integration
endif
endif

.PHONY: test-all
test-all: depends .clean-test ## Run all the tests
	$(NOSE) $(PACKAGES) $(NOSE_OPTS)
ifndef TRAVIS
ifndef APPVEYOR
	$(COVERAGE_SPACE) $(REPOSITORY) overall
endif
endif

.PHONY: read-coverage
read-coverage:
	$(OPEN) htmlcov/index.html

# DOCUMENTATION ################################################################

PDOC_INDEX := docs/apidocs/$(PACKAGE)/index.html
MKDOCS_INDEX := site/index.html

.PHONY: doc
doc: uml pdoc mkdocs ## Run documentation generators

.PHONY: uml
uml: depends docs/*.png ## Generate UML diagrams for classes and packages
docs/*.png: $(MODULES)
	$(PYREVERSE) $(PACKAGE) -p $(PACKAGE) -a 1 -f ALL -o png --ignore tests
	- mv -f classes_$(PACKAGE).png docs/classes.png
	- mv -f packages_$(PACKAGE).png docs/packages.png

.PHONY: pdoc
pdoc: depends $(PDOC_INDEX)  ## Generate API documentaiton with pdoc
$(PDOC_INDEX): $(MODULES)
	$(PDOC) --html --overwrite $(PACKAGE) --html-dir docs/apidocs
	@ touch $@

.PHONY: mkdocs
mkdocs: depends $(MKDOCS_INDEX) ## Build the documentation site with mkdocs
$(MKDOCS_INDEX): mkdocs.yml docs/*.md
	ln -sf `realpath README.md --relative-to=docs` docs/index.md
	ln -sf `realpath CHANGELOG.md --relative-to=docs/about` docs/about/changelog.md
	ln -sf `realpath CONTRIBUTING.md --relative-to=docs/about` docs/about/contributing.md
	ln -sf `realpath LICENSE.md --relative-to=docs/about` docs/about/license.md
	$(MKDOCS) build --clean --strict

.PHONY: mkdocs-live
mkdocs-live: mkdocs ## Launch and continuously rebuild the mkdocs site
	eval "sleep 3; open http://127.0.0.1:8000" &
	$(MKDOCS) serve

# RELEASE ######################################################################

.PHONY: register-test
register-test: README.rst CHANGELOG.rst ## Register the project on the test PyPI
	$(PYTHON) setup.py register --strict --repository https://testpypi.python.org/pypi

.PHONY: register
register: README.rst CHANGELOG.rst ## Register the project on PyPI
	$(PYTHON) setup.py register --strict

.PHONY: upload-test
upload-test: register-test ## Upload the current version to the test PyPI
	$(PYTHON) setup.py sdist upload --repository https://testpypi.python.org/pypi
	$(PYTHON) setup.py bdist_wheel upload --repository https://testpypi.python.org/pypi
	$(OPEN) https://testpypi.python.org/pypi/$(PROJECT)

.PHONY: upload
upload: .git-no-changes register ## Upload the current version to PyPI
	$(PYTHON) setup.py check --restructuredtext --strict --metadata
	$(PYTHON) setup.py sdist upload
	$(PYTHON) setup.py bdist_wheel upload
	$(OPEN) https://pypi.python.org/pypi/$(PROJECT)

.PHONY: .git-no-changes
.git-no-changes:
	@ if git diff --name-only --exit-code;        \
	then                                          \
		echo Git working copy is clean...;        \
	else                                          \
		echo ERROR: Git working copy is dirty!;   \
		echo Commit your changes and try again.;  \
		exit -1;                                  \
	fi;

%.rst: %.md
	pandoc -f markdown_github -t rst -o $@ $<

# CLEANUP ######################################################################

.PHONY: clean
clean: .clean-dist .clean-test .clean-doc .clean-build ## Delete all generated and temporary files

.PHONY: clean-all
clean-all: clean .clean-env .clean-workspace

.PHONY: .clean-build
.clean-build:
	find $(PACKAGES) -name '*.pyc' -delete
	find $(PACKAGES) -name '__pycache__' -delete
	rm -rf *.egg-info

.PHONY: .clean-doc
.clean-doc:
	rm -rf README.rst docs/apidocs *.html docs/*.png site

.PHONY: .clean-test
.clean-test:
	rm -rf .cache .pytest .coverage htmlcov

.PHONY: .clean-dist
.clean-dist:
	rm -rf dist build

.PHONY: .clean-env
.clean-env: clean
	rm -rf $(ENV)

.PHONY: .clean-workspace
.clean-workspace:
	rm -rf *.sublime-workspace

# HELP #########################################################################

.PHONY: help
help: all
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
