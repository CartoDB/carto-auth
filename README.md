# carto-auth

Python library to authenticate with [CARTO](carto.com).

## Install

```bash
pip install carto-auth
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

ca = CartoAuth.from_oauth()

ca.token

cdw = ca.get_carto_dw_client()
```

For more information, check the [examples](./examples) section.

## Development

Make commands:

- init: create the environment and install dependencies
- lint: run linter (black + flake8)
- test: run tests (pytest)
- publish-pypi: publish package in pypi.org
- publish-test-pypi: publish package in test.pypi.org
- clean: remove the environment

## Contributors

- [Jesús Arroyo](https://github.com/jesus89)
- [Óscar Ramírez](https://github.com/tuxskar)
