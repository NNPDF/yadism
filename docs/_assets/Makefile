all:
	@echo
	@echo "To recompile png logos run explicitly 'make inkscape' in '_assets'."
	@echo

.PHONY: all inkscape logo

inkscape: n3pdf_badge.png n3pdf_logo.png logo

n3pdf_logo.png: n3pdf_logo.svg
	inkscape $< --export-png $@ -w 1200

n3pdf_badge.png: n3pdf_badge.svg
	inkscape $< --export-png $@ -w 1200

logo:
	cd logo && make
