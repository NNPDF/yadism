DEMODIR=demo/yadism

.PHONY: all, demo, view, clean, home-page, assets, sphinx-html, demo-dir

all: demo

demo: home-page assets sphinx-html

demo-dir:
	@mkdir -p $(DEMODIR)

home-page: demo-dir
	cd home-page && echo ${PWD} && make
	cp -r home-page/build/* $(DEMODIR)

assets: demo-dir
	cp -r _assets $(DEMODIR)

sphinx-html: demo-dir
	cd sphinx && echo ${PWD} &&make html
	cp -r sphinx/build/html $(DEMODIR)
	@mv $(DEMODIR)/html $(DEMODIR)/develop

view:
	@python3 -m http.server 8000 --directory demo &
	${BROWSER} localhost:8000

clean:
	cd sphinx && make clean
	cd home-page && make clean
	rm -rf demo
