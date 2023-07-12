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

This should download and install the latest version of Python 3.11.

## Installation for development

1. Clone the "scutes" Git repository:

    ```zsh
    git clone git@github.com:timkanke/scutes.git
    ```

2. Switch to the "scutes" directory:

    ```zsh
    cd scutes
    ```

3. Verify that the Python version is 3.11:

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

6. Install web drivers in .venv/bin:

   ```zsh
   python setup-webdrivers.py
   ```

## Running the tests

```zsh
pytest --driver Firefox
# or
pytest --driver Chrome
```

**Note:** To restrict pytest test discovery to just the "tests" directory, run

```zsh
pytest tests
```

## Code Style

Application code style should generally conform to the guidelines in [PEP 8]. The
"pycodestyle" tool to check compliance with the guidelines can be run using:

```zsh
pycodestyle .
```
