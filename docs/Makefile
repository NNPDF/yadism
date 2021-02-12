DEMODIR=demo/yadism

.PHONY: all, demo, view, clean, home, assets, sphinx-html, demo-dir

all: demo
	@# all - compile everything in `demo`

demo: home assets sphinx-html

demo-dir:
	@mkdir -p $(DEMODIR)

home: demo-dir
	cd home-page && echo ${PWD} && make
	cp -r home-page/build/* $(DEMODIR)

assets: demo-dir
	cd _assets && make
	cp -r _assets $(DEMODIR)

sphinx-html: demo-dir
	cd sphinx && echo ${PWD} &&make html
	cp -r sphinx/build/html $(DEMODIR)
	@rm -rf $(DEMODIR)/develop
	@mv $(DEMODIR)/html $(DEMODIR)/develop

view: kill-server
	@# view - Open result in default browser
	@python3 -m http.server 8000 --directory demo & echo "$$!" > .server
	${BROWSER} localhost:8000

kill-server:
	@# kill-server - kill running python server
ifneq (,$(wildcard ./.server))
	@echo "Kill server at PID:$$(cat .server)"
	-@kill $$(cat .server)
	@rm -f .server
endif

clean-demo:
	@# clean-demo - Clean final product only
	rm -rf demo

clean: clean-demo
	@# clean - Clean everything (nested)
	cd sphinx && make clean
	cd home-page && make clean
	rm -rf demo

help:
	@# help - Show this help.
	@./MakefileHelp.sh
