# Makefile for demjson
# This is a simple installation front-end for Unix-like machines.
# See the INSTALL.txt file for specific instructions.

PYTHON=python
PYDOC=pydoc

MODULE=demjson
VERSION=1.7

SOURCES = $(MODULE).py
SETUP = setup.py
READMES = README.txt LICENSE.txt docs/AUTHORS.txt docs/CHANGES.txt docs/INSTALL.txt docs/NEWS.txt
TESTS = test/test_$(MODULE).py
#DOCS = docs/$(MODULE).html docs/$(MODULE).txt docs/jsonlint.txt
DOCS = docs/$(MODULE).txt docs/jsonlint.txt
SCRIPTS = jsonlint
DISTDIR = dist

DIST_FILE = $(DISTDIR)/$(MODULE)-$(VERSION).tar.gz
ALL_FILES = $(SOURCES) $(SETUP) $(READMES) $(TESTS) $(DOCS) $(SCRIPTS)

all: build test install

ALWAYS:

show:
	@for f in $(ALL_FILES) ; do \
	   echo $$f ; \
	done | sort -u

#MANIFEST.in: $(ALL_FILES) Makefile
#	rm -f $@
#	for f in $(ALL_FILES) ; do \
#	   echo include $$f ; \
#	done | sort -u > $@

dist:   $(DIST_FILE)
	@ls -l -- $(DIST_FILE)

clean:
	rm *.pyc
	rm -r build

build: $(SOURCES) $(SETUP)
	$(PYTHON) $(SETUP) build

install: $(SOURCES) $(SETUP)
	$(PYTHON) $(SETUP) install

register: $(DISTDIR)/$(MODULE)-$(VERSION).tar.gz $(SETUP)
	$(PYTHON) $(SETUP) register

test: ALWAYS $(SOURCES) $(TESTS)
	(cd test && PYTHONPATH=.. $(PYTHON) test_$(MODULE).py)
	echo done

$(DIST_FILE): MANIFEST.in $(ALL_FILES)
	$(PYTHON) setup.py sdist -d $(DISTDIR)

docs: $(DOCS) ALWAYS

docs/jsonlint.txt: jsonlint
	PYTHONPATH=. ./jsonlint --help >$@

docs/$(MODULE).txt:     $(MODULE).py
	pydoc $(MODULE) | sed -e 's|/home/dem/.*/||' >docs/$(MODULE).txt

docs/$(MODULE).html:    $(MODULE).py
	$(PYDOC) -w $(MODULE)
	sed -e 's|file:/home/dem/public_html|http://deron.meranda.us|g' \
	   -e 's|>/home/dem/public_html/python/$(MODULE)/[0-9.]*/|>|g' \
	   -e 's|http://deron.meranda.us/[a-zA-Z0-9_/.-]*/||g' \
	<$(MODULE).html >docs/$(MODULE).html
	rm -f $(MODULE).html

