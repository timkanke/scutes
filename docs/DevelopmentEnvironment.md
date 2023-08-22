# Development Environment

## Introduction

This page describes how to set up a development environment, and other
information useful for developers to be aware of.

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

## Installation for development

1. Clone the "scutes" Git repository:

    ```zsh
    git clone git@github.com:timkanke/scutes.git
    ```

2. Switch to the "scutes" directory:

    ```zsh
    cd scutes
    ```

3. Verify that the Python version is correct:

    ```zsh
    pyenv version
    ```

4. Create and activate the virtual environment:

   ```zsh
   python -m venv .venv
   source .venv/bin/activate
   ```

5. Install all dependencies and configure the `scutes` entrypoint:

   ```zsh
   pip install -r requirements.dev.txt -e .
   ```

6. Install web drivers in ```.venv/bin```:

   ```zsh
   python setup-webdrivers.py
   ```

7. For local development, create a ```src/.env```. Or change ```src/.env-dev``` to ```src/.env```.
    The settings in the file are:

    ```env
    DEBUG=on
    ALLOWED_HOSTS=localhost,127.0.0.1
    SECRET_KEY='your-secret-key'
    DATABASE_URL=sqlite:///./db.sqlite3
    ```

## Running the tests

```zsh
pytest --driver Firefox
# and/or
pytest --driver Chrome
```

To skip tests that require webdrivers:

```zsh
pytest -m "not webdriver"
```

**Note:** To restrict pytest test discovery to just the "tests" directory, run:

```zsh
pytest tests
```

## Code Style

Application code style should generally conform to the guidelines in [PEP 8]. The
"pycodestyle" tool checks for compliance with the guidelines. It can be ran using:

```zsh
pycodestyle .
```
