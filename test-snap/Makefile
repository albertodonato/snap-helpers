BASE ?= core22

.DEFAULT_GOAL := snap

setup: snap-helpers snapcraft.yaml
.PHONY: setup

snap: setup
	SNAPCRAFT_BUILD_ENVIRONMENT=lxd snapcraft
.PHONY: snap

clean:
	rm -rf snap-helpers snapcraft.yaml *.snap
.PHONY: clean

snap-helpers:
	mkdir -p $@
	cp -a ../pyproject.toml ../snaphelpers $@
.PHONY: snap-helpers

snapcraft.yaml:
	tox run -e test-snap-snapcraft-yaml -- $(BASE)
.PHONY: snapcraft.yaml
