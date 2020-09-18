# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

SRCDIR = ../../src/yadism

TODOOUTFILE = ./source/dev-tools/code-todos.rst

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help html view clean cleanall

html: todos
	sphinx-apidoc -o ./source/modules --module-first $(SRCDIR)
	@rm -f ./source/modules/modules.rst ./source/modules/*/modules.rst}
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

view: html
	$(BROWSER) $(BUILDDIR)/html/index.html

server: html
	python3 -m http.server 8000 --bind 127.0.0.1 --directory build/html &
	$(BROWSER) 127.0.0.1:8000/index.html

clean:
	rm -rf build
	rm -rf _build

cleanall: clean clean-todos
	rm -rf $(SOURCEDIR)/modules

# TODOs
todos:
	python generate_code_todos.py "$(SRCDIR)" "$(TODOOUTFILE)"

clean-todos:
	rm "$(TODOOUTFILE)"
