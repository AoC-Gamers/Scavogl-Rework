.DEFAULT_GOAL := help

ifeq ($(OS),Windows_NT)
PYTHON ?= python
SMX_PLATFORM ?= windows
SPCOMP_NAME := spcomp.exe
else
PYTHON ?= $(shell command -v python3 >/dev/null 2>&1 && echo python3 || echo python)
SMX_PLATFORM ?= linux
SPCOMP_NAME := spcomp
endif

# Support make -f from a different directory, including paths that contain spaces.
ROOT_DIR := $(shell $(PYTHON) -c "import sys; from pathlib import Path; print(Path(sys.argv[1]).resolve().parent.as_posix())" "$(MAKEFILE_LIST)")

SOURCEMOD_VERSION ?= 1.12
SPCOMP ?= .deps/smx/sourcemod-$(SMX_PLATFORM)/addons/sourcemod/scripting/$(SPCOMP_NAME)
SMX_BUILD_DIR ?= .build/smx
SMX_COMPILE_LOG ?= .build/build-smx-compile.log
RUN = cd "$(ROOT_DIR)" && $(PYTHON)

RELEASE_BASENAME ?= scavogl-rework-local
PACKAGE = $(RUN) scripts/package/artifact_contract.py

.PHONY: help deps-smx build-smx validate-modes package-modes release validate-artifact
help:
	@$(RUN) -c "print('deps-smx, build-smx, validate-modes, package-modes, release, validate-artifact')"

deps-smx:
	$(RUN) scripts/deps/fetch-sourcemod.py --root . --platform "$(SMX_PLATFORM)" --version "$(SOURCEMOD_VERSION)" --archive-url "$(SOURCEMOD_ARCHIVE_URL)"

build-smx:
	$(RUN) scripts/build/build-local.py --root . --spcomp "$(SPCOMP)" --output-root "$(SMX_BUILD_DIR)" --compile-log "$(SMX_COMPILE_LOG)"

validate-modes:
	$(PACKAGE) validate-modes

package-modes:
	$(PACKAGE) package-modes --build-dir "$(SMX_BUILD_DIR)"

release: package-modes
	$(PACKAGE) release --build-dir "$(SMX_BUILD_DIR)" --basename "$(RELEASE_BASENAME)"

validate-artifact:
	$(PACKAGE) validate-artifact --build-dir "$(SMX_BUILD_DIR)" --basename "$(RELEASE_BASENAME)"
