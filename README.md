PythonTemplateDemo
======
A sample project templated from jacebrowning/template-python.

[![Build Status](http://img.shields.io/travis/jacebrowning/template-python-demo/master.svg)](https://travis-ci.org/jacebrowning/template-python-demo)
[![Coverage Status](http://img.shields.io/coveralls/jacebrowning/template-python-demo/master.svg)](https://coveralls.io/r/jacebrowning/template-python-demo)
[![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/jacebrowning/template-python-demo.svg)](https://scrutinizer-ci.com/g/jacebrowning/template-python-demo/?branch=master)
[![PyPI Version](http://img.shields.io/pypi/v/PythonTemplateDemo.svg)](https://pypi.python.org/pypi/PythonTemplateDemo)
[![PyPI Downloads](http://img.shields.io/pypi/dm/PythonTemplateDemo.svg)](https://pypi.python.org/pypi/PythonTemplateDemo)


Getting Started
===============

Requirements
------------

* Python 2.7+ or Python 3.3+

Installation
------------

PythonTemplateDemo can be installed with pip:

```
$ pip install PythonTemplateDemo
```

or directly from the source code:

```
$ git clone https://github.com/jacebrowning/template-python-demo.git
$ cd template-python-demo
$ python setup.py install
```

Basic Usage
===========

After installation, the package can imported:

```
$ python
>>> import demo
>>> demo.__version__
```

PythonTemplateDemo doesn't do anything, it's a template.

For Contributors
================

Requirements
------------

* Make:
    * Windows: http://cygwin.com/install.html
    * Mac: https://developer.apple.com/xcode
    * Linux: http://www.gnu.org/software/make (likely already installed)
* virtualenv: https://pypi.python.org/pypi/virtualenv#installation
* Pandoc: http://johnmacfarlane.net/pandoc/installing.html
* Graphviz: http://www.graphviz.org/Download.php

Installation
------------

Create a virtualenv:

```
$ make env
```

Run the tests:

```
$ make test
$ make tests  # includes integration tests
```

Build the documentation:

```
$ make doc
```

Run static analysis:

```
$ make pep8
$ make pep257
$ make pylint
$ make check  # includes all checks
```

Prepare a release:

```
$ make dist  # dry run
$ make upload
```
