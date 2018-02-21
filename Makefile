
SHELL:=/bin/bash
ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY: all clean dependencies package

all: dependencies

clean:
	rm -rf $(ROOT_DIR)/*.pyc
	rm -rf $(ROOT_DIR)/venv
	rm -rf $(ROOT_DIR)/dist
	rm -rf $(ROOT_DIR)/build
	rm -rf $(ROOT_DIR)/*.egg-info

dependencies:
	if [ ! -d $(ROOT_DIR)/env ]; then python3 -m venv $(ROOT_DIR)/venv; fi
	set -e; source $(ROOT_DIR)/venv/bin/activate; yes w | python -m pip install -e .[dev]

package:
	set -e; source $(ROOT_DIR)/venv/bin/activate; python setup.py bdist_wheel
