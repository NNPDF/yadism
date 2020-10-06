all: logo-favicon.pdf logo-favicon.png logo-favicon-16x16.png logo-favicon-32x32.png logo-docs.png logo.png

.PHONY: all

logo-favicon.pdf: logo-favicon.svg
	inkscape --file=$< --export-area-drawing --without-gui --export-pdf=$@

logo-favicon.png: logo-favicon.svg
	inkscape $< --export-png $@

logo-favicon-16x16.png: logo-favicon.svg
	inkscape $< --export-png $@ -w 16

logo-favicon-32x32.png: logo-favicon.svg
	inkscape $< --export-png $@ -w 32

logo-docs.png: logo-docs.svg
	inkscape $< --export-png $@ -w 3351

logo.png: logo.svg
	inkscape $< --export-png $@ -w 3610
