PWD=$(dir $(realpath $(lastword $(MAKEFILE_LIST))))
export PATH:=$(PATH):$(PWD)/node_modules/.bin/

TS_SOURCES=$(wildcard medtech_api/static-src/*.ts)
JS_TARGETS=$(subst static-src/,static/,$(TS_SOURCES:%.ts=%.js))

HTML_SOURCES=$(wildcard medtech_api/static-src/*.html)
HTML_TARGETS=$(subst static-src/,static/,$(HTML_SOURCES))


.PHONY: all js html

all: js html

js: $(JS_TARGETS)

html: $(HTML_TARGETS)

medtech_api/static/%.html: medtech_api/static-src/%.html
	cp "$<" "$@"

medtech_api/static/%.js: medtech_api/static-src/%.ts
	tsc --out "$@" "$<"
