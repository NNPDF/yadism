IMAGES=$(wildcard *.svg)

.PHONY: png


png: $(patsubst %.svg,%.png,$(IMAGES))

pdf: $(patsubst %.svg,%.pdf,$(IMAGES))

%.png: %.svg
	inkscape $< --export-filename=$@ -w 1200

%.pdf: %.svg
	inkscape --file=$< --export-area-drawing --without-gui --export-pdf=$@
