
setup:
    python -m venv .venv

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

lint:
	pylint --disable=R,C compare_dataframe.py, main.py

test:
	python -m pytest -vv --cov=compare_dataframe compare_dataframe.py
	    
