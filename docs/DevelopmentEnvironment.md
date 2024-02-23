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

    If not correct version, set python version to local directory

    ```zsh
    pyenv local 3.11
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

7. For local development, the ```src/.env``` file is required.
Copy and rename ```src/.env-dev-example``` to ```src/.env```.

8. Add key and crt files to src/scutes directory.

## Set up

1. If not in src directory, then change into src directory:

    ```zsh
    cd src
    ```

2. Run migrate command:

    ```zsh
    ./manage.py migrate
    ```

3. Run createsuperuser command:

    ```zsh
    ./manage.py createsuperuser
    ```

4. Import Data
    Use either YAML test data or an .mbox file
    See Management Commands

5. Edit your "/etc/hosts" file:

    ```zsh
    sudo vi /etc/hosts
    ```

    and add "scutes-local" aliases to the "127.0.0.1" entry:

    ```
    127.0.0.1       localhost scutes-local
    ```

6. To Start the dev server. Run manage command in src directory.

    ```zsh
    ./manage.py runserver
    ```

    Note: Use ctrl+c to stop server. If server command prompt is given back without stopping the server, you will need to kill the process in order to see logging. For example, you accidentally hit ctrl-z.

    ```zsh
    lsof -t -i tcp:8000 | xargs kill -9
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
