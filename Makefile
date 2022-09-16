VENV=env
DIST=dist
BUILD=build
BIN=$(VENV)/bin

.PHONY: docs

init:
	test `command -v python3` || echo Please install python3
	[ -d $(VENV) ] || python3 -m venv $(VENV)
	$(BIN)/pip install -r requirements_dev.txt
	$(BIN)/pip install -e .

lint:
	$(BIN)/black carto_auth tests examples setup.py
	$(BIN)/flake8 carto_auth tests examples setup.py

test:
	$(BIN)/pytest tests

docs:
	$(BIN)/lazydocs carto_auth --validate --output-path="docs" --overview-file="README.md"

publish-pypi:
	rm -rf $(DIST) $(BUILD) *.egg-info
	$(BIN)/python setup.py sdist bdist_wheel
	$(BIN)/twine upload $(DIST)/*

publish-test-pypi:
	rm -rf $(DIST) $(BUILD) *.egg-info
	$(BIN)/python setup.py sdist bdist_wheel
	$(BIN)/twine upload --repository-url https://test.pypi.org/legacy/ $(DIST)/* --verbose

clean:
	rm -rf $(VENV) $(DIST) $(BUILD) *.egg-info
