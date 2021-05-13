# Run `watch -n1 make`

#files := $(shell xargs -a COMPILELIST.TXT)
pdf_output := $(patsubst %.md,%.pdf,$(wildcard *.md))

all: $(pdf_output)

%.pdf: %.md
	pandoc --toc -f markdown -t pdf -s $< -o $@

#%.html: %.mdp
	#pandoc --toc -f markdown -t html -c style.css -s $< -o $@
