all: write_defaults write_constants plot_example

write_defaults:
	sh -c '. ./venv/bin/activate; ./scripts/write_defaults.py'

write_constants:
	sh -c './scripts/write_constants_py.sh > pyhector/constants.py'

plot_example:
		sh -c '. ./venv/bin/activate; pip install matplotlib; python scripts/plot_example.py'

watchdocs:
	sh -c '. ./venv/bin/activate; sphinx-autobuild \
	--watch ../pyhector \
	--ignore "*.lock" \
	docs docs/_build/html;'

venv: dev-requirements.txt
	[ -d ./venv ] || python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -Ur dev-requirements.txt
	./venv/bin/pip install -Ur docs/requirements.txt

test-pypi-install:
	$(eval TEMPVENV := $(shell mktemp -d))
	python3 -m venv $(TEMPVENV)
	$(TEMPVENV)/bin/pip install pip --upgrade
	$(TEMPVENV)/bin/pip install pyhector
	$(TEMPVENV)/bin/python -c "import sys; sys.path.remove(''); import pyhector; print(pyhector.__version__)"


.PHONY: watchdocs write_defaults write_constants plot_example test-pypi-install

