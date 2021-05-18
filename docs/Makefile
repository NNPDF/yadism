# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

SRCDIR = ../src/yadism
YADISMOUT = $(SOURCEDIR)/modules
YADMARKDIR = ../benchmarks/yadmark
YADMARKOUT = $(SOURCEDIR)/dev-tools/yadmark

TODOOUTFILE = ./source/dev-tools/code-todos.rst

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help html view clean clean-todos cleanall

html: todos
	sphinx-apidoc -o $(YADISMOUT) --module-first $(SRCDIR)
	@rm -f $(YADISMOUT)/modules.rst
	sphinx-apidoc -o $(YADMARKOUT) --module-first $(YADMARKDIR)
	@rm -f $(YADMARKOUT)/modules.rst
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

view:
	$(BROWSER) $(BUILDDIR)/html/index.html

server:
	python3 -m http.server 8000 --bind 127.0.0.1 --directory build/html &
	$(BROWSER) 127.0.0.1:8000/index.html

clean:
	rm -rf build
	rm -rf _build

cleanall: clean clean-todos
	rm -rf $(YADISMOUT)
	rm -rf $(YADMARKOUT)

# TODOs
todos:
	python generate_code_todos.py "$(SRCDIR)" "$(TODOOUTFILE)"

clean-todos:
	rm "$(TODOOUTFILE)"
