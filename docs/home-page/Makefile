SASS="./node_modules/dart-sass/sass.js"

.PHONY: all html css _js view clean

all: html css _js

html: build/index.html

css: build/home.css

_js: build/js

build:
	@mkdir -p build

build/index.html: index.html.jinja build
	@echo "\e[1m\e[4m\e[35mFilling HTML templates:\e[0m"
	python3 compile_template.py $< $@
	@echo

build/home.css: home.scss build
	@echo "\e[1m\e[4m\e[35mCompiling CSS from SASS:\e[0m"
	${SASS} --no-source-map $< $@
	@echo
	
build/js: js build
	@echo "\e[1m\e[4m\e[35mProviding Javascript:\e[0m"
	cp -r $< $@
	@echo

view:
	@${BROWSER} build/index.html

clean:
	rm -rf build
