all: write_defaults write_constants plot_example

write_defaults: venv
	sh -c '. ./venv/bin/activate; ./scripts/write_defaults.py'

write_constants: venv
	sh -c './scripts/write_constants_py.sh > pyhector/constants.py'

plot_example: venv
		sh -c '. ./venv/bin/activate; pip install matplotlib; python scripts/plot_example.py'

watchdocs: venv
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
	-rm -rf build dist
	@status=$$(git status --porcelain); \
	if test "x$${status}" = x; then \
		./venv/bin/python setup.py sdist; \
		./venv/bin/twine upload dist/*; \
	else \
		echo Working directory is dirty >&2; \
	fi;

test-pypi-install:
	$(eval TEMPVENV := $(shell mktemp -d))
	python3 -m venv $(TEMPVENV)
	$(TEMPVENV)/bin/pip install pip --upgrade
	$(TEMPVENV)/bin/pip install pyhector
	$(TEMPVENV)/bin/python -c "import sys; sys.path.remove(''); import pyhector; print(pyhector.__version__)"

publish-on-testpypi:
	-rm -rf build dist
	@status=$$(git status --porcelain); \
	if test "x$${status}" = x; then \
		./venv/bin/python setup.py sdist; \
		./venv/bin/twine upload -r testpypi dist/*; \
	else \
		echo Working directory is dirty >&2; \
	fi;

test-testpypi-install:
	$(eval TEMPVENV := $(shell mktemp -d))
	python3 -m venv $(TEMPVENV)
	$(TEMPVENV)/bin/pip install pip --upgrade
	# Install dependencies, because these are not on testpypi registry
	$(TEMPVENV)/bin/pip install pandas pybind11
	# Install pyhector without dependencies.
	$(TEMPVENV)/bin/pip install \
		-i https://testpypi.python.org/pypi pyhector \
		--no-dependencies
	# Remove local directory from path to get actual installed version.
	$(TEMPVENV)/bin/python -c "import sys; sys.path.remove(''); import pyhector; print(pyhector.__version__)"

.PHONY: watchdocs write_defaults write_constants plot_example publish-on-pypi test-pypi-install publish-on-testpypi test-testpypi-install
