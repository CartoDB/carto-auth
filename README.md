# carto-auth

[![PyPI version](https://badge.fury.io/py/carto-auth.svg)](https://badge.fury.io/py/carto-auth)
[![PyPI downloads](https://img.shields.io/pypi/dm/carto-auth.svg)](https://pypistats.org/packages/carto-auth)
[![Tests](https://github.com/cartodb/carto-auth/actions/workflows/ci.yml/badge.svg)](https://github.com/cartodb/carto-auth/actions)

Python library to authenticate with [CARTO](carto.com).

## Install

```bash
pip install carto-auth
```

To install the CARTO DW extension:

```bash
pip install carto-auth[carto-dw]
```

### Installing from source

```bash
git clone https://github.com/cartodb/carto-auth
cd carto-auth
pip install .
```

## Usage

```py
from carto_auth import CartoAuth

# Authentication
carto_auth = CartoAuth.from_oauth()
# carto_auth = CartoAuth.from_file("./carto_credentials.json")

# Get access token
access_token = carto_auth.get_access_token()

# CARTO Data Warehouse
carto_dw_project, carto_dw_token = carto_auth.get_carto_dw_credentials()
carto_dw_client = carto_auth.get_carto_dw_client()
```

For more information, check the [examples](./examples) section.

## Development

Make commands:

- init: create the environment and install dependencies
- lint: run linter (black + flake8)
- test: run tests (pytest)
- docs: build the documentation
- publish-pypi: publish package in pypi.org
- publish-test-pypi: publish package in test.pypi.org
- clean: remove the environment

Check the development [documentation](./docs) section.

## Contributors

- [Jesús Arroyo](https://github.com/jesus89)
- [Óscar Ramírez](https://github.com/tuxskar)
