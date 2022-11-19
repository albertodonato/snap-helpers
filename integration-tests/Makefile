BASE ?= core22

.DEFAULT_GOAL := setup

setup: snap-helpers snapcraft.yaml
.PHONY: setup

clean:
	rm -rf snap-helpers snapcraft.yaml
.PHONY: setup

test:
	testapp.pytest -vvs tests.py
.PHONY:test

snap-helpers:
	mkdir -p $@
	cp -a ../setup.* ../snaphelpers $@
.PHONY: snap-helpers

snapcraft.yaml: snapcraft-$(BASE).yaml
	rm -f $@
	ln -sf $< $@
.PHONY: snapcraft.yaml
