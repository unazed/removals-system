VENV 	= .venv
SQLDIR  = db
PYTHON 	= $(VENV)/bin/python3
PIP 	= $(VENV)/bin/pip
DB		= psql
DBNAME  = removals

run: $(VENV)/bin/activate
	$(PYTHON) main.py

$(VENV)/bin/activate: requirements.txt
	@command -v python3 -v > /dev/null || (echo "Error: `python3` not found on your system." && exit 1)
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf $(VENV)

clean-db:
	$(DB) -f $(DB)/init/clear_schema.sql $(DBNAME) --username=postgres

init-db:
	$(DB) -f $(DB)/init/init_schema.sql $(DBNAME) --username=postgres

.PHONY: run clean