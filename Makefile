VENV 	= .venv
SQLDIR  = db
PYTHON 	= $(VENV)/bin/python
PIP 	= $(VENV)/bin/pip
DB		= psql
DBNAME  = removals
SYSPYTHON = python

run: $(VENV)/bin/activate
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) main.py

$(VENV)/bin/activate: requirements.txt
	@command -v $(SYSPYTHON) -v > /dev/null || (echo "Error: `python3` not found on your system." && exit 1)
	$(SYSPYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf $(VENV)

clean-db:
	$(DB) -f $(DB)/init/clear_schema.sql $(DBNAME) --username=postgres

init-db:
	$(DB) -f $(DB)/init/init_schema.sql $(DBNAME) --username=postgres

.PHONY: run clean