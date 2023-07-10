.PHONY: setup, serve, debug

setup:
	source venv/bin/activate && pip install -r api/requirements.txt

serve:
	source venv/bin/activate && cd api/src && flask run -p 6608

debug:
	source venv/bin/activate && cd api/src && flask run --debug -p 6608
