# Run `watch -n1 make`

#files := $(shell xargs -a COMPILELIST.TXT)
pdf_output := $(patsubst %.mdp,%.pdf,$(wildcard *.mdp))

all: $(pdf_output)

%.pdf: %.mdp
	pandoc --toc -f markdown -t pdf -s $< -o $@

#%.html: %.mdp
	#pandoc --toc -f markdown -t html -c style.css -s $< -o $@
