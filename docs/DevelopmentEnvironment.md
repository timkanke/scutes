# Development Environment

## Introduction

This document provides guidance on setting up a Scutes development environment on a local workstation.

## Prerequisites

The following instructions assume that "pyenv" is installed to enable
the setup of an isolated Python environment.

See the following for setup instructions:

* <https://github.com/pyenv/pyenv>

Once "pyenv" have been installed, install Python 3.11:

```zsh
pyenv install 3.11
```

This should download and install that version of Python.

## Setup

Clone Scutes from GitHub:

```bash
git clone git@github.com:umd-lib/scutes
cd scutes
python -m venv --prompt "scutes-py$(cat .python-version)" .venv
source .venv/bin/activate
pip install -e .
```

Install `libxmlsec1`. This is required for the SAML authentication using
[djangosaml2].

On Mac, it is available via Homebrew:

```bash
brew install xmlsec1
```

On Debian or Ubuntu Linux, it is available via `apt`:

```bash
sudo apt-get install xmlsec1
```

Update the `/etc/hosts` file to add:

```
127.0.0.1   localhost scutes-local
```

Add key and crt files to src/scutes directory.

Setup env file.
Copy/rename ```src/.env-dev-example``` to ```src/.env``` and make adjustments as necessary.

## Initalize the database

In src directory, run migrate command:

```zsh
./manage.py migrate
```

Import Data
    Use either YAML test data or an .mbox file
    See Management Commands

## Start the dev server

```zsh
./manage.py runserver
```

The application will be running at <http://scutes-local:15000/>
Note: Use ctrl+c to stop the server. If the prompt is given back without stopping the server, you will need to kill the process.

```zsh
lsof -t -i tcp:15000 | xargs kill -9
```

### Tests

To install test dependencies, install the `test` extra:

```bash
pip install -e .[test]
```

This project uses [pytest] in conjunction with the [pytest-django] plugin
to run its tests. To run the test suite:

```bash
pytest
```

To run with coverage information:

```bash
pytest --cov src --cov-report term-missing
```

To load YAML test data

```zsh
./manage.py loaddata test_data
```
