SASS="./node_modules/dart-sass/sass.js"
JINJA_BLOCKS=$(filter-out jinja/index.html.jinja, $(wildcard jinja/*.html.jinja)) 

all: html css _js

.PHONY: all html css _js view clean

html: build/index.html

css: build/home.css

_js: build/js

build:
	@mkdir -p build

build/index.html: jinja/index.html.jinja build $(JINJA_BLOCKS)
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

