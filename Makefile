test:
	python -m nose $(NOSE_ARGS)

fix:
	autopep8 --in-place -r -a webapp
	autopep8 --in-place -r -a algos
	autopep8 --in-place -r -a tests
	autopep8 --in-place -r -a examples

coverage:
	python -m coverage run --source=webapps -m nose
	python -m coverage run --source=algos -m nose
	python -m coverage html

dist:
	python setup.py sdist bdist_wheel

release:
	python3 -m twine upload dist/*

clean:
	rm -rf build dist docs-build *.egg-info
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	find . -type d -name .pytest_cache -delete

apidoc:
	sphinx-apidoc -o docs margot


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