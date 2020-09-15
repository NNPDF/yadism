# Run `watch -n1 make`

#files := $(shell xargs -a COMPILELIST.TXT)
files := q_ns.md

q_ns.pdf: $(files)
	#pandoc $(files) --toc -f markdown -t html -c style.css -o $@
	pandoc -s $(files) -o $@
