test:
	pytest

fix:
	autopep8 --in-place -r -a margot

coverage:
	python -m coverage run --source=margot -m nose
	python -m coverage html

release:
	python setup.py sdist bdist_wheel upload
	twine upload dist/*

clean:
	rm -rf build dist docs-build *.egg-info
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	find . -type d -name .pytest_cache -delete

apidoc:
	sphinx-apidoc -feo docs margot


##################
# Sphinx for documentation
##################
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs
BUILDDIR      = docs-build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
