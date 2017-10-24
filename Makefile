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
	./venv/bin/pip install wheel
	./venv/bin/pip install -Ur dev-requirements.txt

publish-on-pypi:
	python setup.py register -r https://pypi.python.org/pypi
	python setup.py sdist upload -r https://pypi.python.org/pypi

test-pypi-install:
	$(eval TEMPVENV := $(shell mktemp -d))
	python3 -m venv $(TEMPVENV)
	$(TEMPVENV)/bin/pip install pip --upgrade
	$(TEMPVENV)/bin/pip install pyhector
	$(TEMPVENV)/bin/python -c "import sys; sys.path.remove(''); import pyhector; print(pyhector.__version__)"

publish-on-testpypi:
	python setup.py register -r https://testpypi.python.org/pypi
	python setup.py sdist upload -r https://testpypi.python.org/pypi

test-testpypi-install:
	$(eval TEMPVENV := $(shell mktemp -d))
	python3 -m venv $(TEMPVENV)
	$(TEMPVENV)/bin/pip install pip --upgrade
	# Install dependencies not on testpypi registry
	$(TEMPVENV)/bin/pip install pandas
	# Install pyhector without dependencies.
	$(TEMPVENV)/bin/pip install \
		-i https://testpypi.python.org/pypi pyhector \
		--no-dependencies
	# Remove local directory from path to get actual installed version.
	$(TEMPVENV)/bin/python -c "import sys; sys.path.remove(''); import pyhector; print(pyhector.__version__)"

.PHONY: watchdocs write_defaults write_constants plot_example publish-on-pypi test-pypi-install publish-on-testpypi test-testpypi-install

