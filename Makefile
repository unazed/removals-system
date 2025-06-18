VENV ?= .venv
SYSPYTHON ?= python

ifeq ($(OS),Windows_NT)
    ACTIVATE = $(VENV)/Scripts/activate
    PYTHON   = $(VENV)/Scripts/python.exe
    PIP      = $(VENV)/Scripts/pip.exe
else
    ACTIVATE = $(VENV)/bin/activate
    PYTHON   = $(VENV)/bin/python
    PIP      = $(VENV)/bin/pip
endif

run: $(ACTIVATE)
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) main.py

$(ACTIVATE): requirements.txt
	@command -v $(SYSPYTHON) >/dev/null || (echo "Error: python not found on your system." && exit 1)
	$(SYSPYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

DB       ?= removals
HOST     ?= localhost
PORT     ?= 5432
USER     ?= postgres
PASS     ?= postgres
SCHEMA   ?= public
OUTPUT   ?= graph-html
JAR      ?= ext/schemaspy.jar
JDBC     ?= ext/postgresql.jar

gen-graph:
	java -jar $(JAR) \
		-t pgsql11 \
		-dp $(JDBC) \
		-db $(DB) \
		-host $(HOST) \
		-port $(PORT) \
		-u $(USER) \
		-p $(PASS) \
		-s $(SCHEMA) \
		-vizjs \
		-o $(OUTPUT)

check-goose:
	@command -v goose >/dev/null || (echo "Error: goose is not installed or not in PATH." && exit 1)

clean:
	rm -rf __pycache__
	rm -rf $(VENV)

clean-db: check-goose
	goose -dir=migrations/seed -no-versioning reset
	goose reset

init-db: check-goose
	goose up
	goose -dir=migrations/seed -no-versioning up

.PHONY: run clean clean-db init-db gen-graph
