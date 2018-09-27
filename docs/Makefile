# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = pyhector
SOURCEDIR     = .
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help \
		Makefile \
		sources/emissions_mapping.py \
		sources/output_variables.py \
		sources/units_dict.py

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile static/emissions_mapping.inc static/output_variables.inc static/units_dict.inc
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

static/emissions_mapping.inc: sources/emissions_mapping.py
	@python $< $@

static/output_variables.inc: sources/output_variables.py
	@python $< $@

static/units_dict.inc: sources/units_dict.py
	@python $< $@
