PWD=$(dir $(realpath $(lastword $(MAKEFILE_LIST))))
export PATH:=$(PATH):$(PWD)/node_modules/.bin/

TS_SOURCES=$(wildcard medtech_api/static-src/*.ts)
JS_TARGETS=$(subst static-src/,static/,$(TS_SOURCES:%.ts=%.js))

HTML_SOURCES=$(wildcard medtech_api/static-src/*.html)
HTML_TARGETS=$(subst static-src/,static/,$(HTML_SOURCES))

ASSETS_SOURCES=$(wildcard medtech_api/assets/*)
ASSETS_TARGETS=$(subst /assets/,/static/,$(ASSETS_SOURCES))

.PHONY: all js html assets

all: js html assets

js: $(JS_TARGETS)

medtech_api/static/%.js: medtech_api/static-src/%.ts
	mkdir -p "$(@D)"
	mkdir -p medtech_api/build
	tsc -t ES6 --out "medtech_api/build/$*.js" "$<"
	babel "medtech_api/build/$*.js" -o "$@"

html: $(HTML_TARGETS)

medtech_api/static/%.html: medtech_api/static-src/%.html
	mkdir -p "$(@D)"
	cp "$<" "$@"

assets: $(ASSETS_TARGETS)

$(ASSETS_TARGETS): medtech_api/static/%: medtech_api/assets/%
	mkdir -p "$(@D)"
	cp "$<" "$@"

