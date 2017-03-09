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

.PHONY: watchdocs write_defaults write_constants plot_example

