setup: 
	python3 -m venv .venv

install:
	python3 -m pip install --upgrade pip 
	python3 -m pip install -r requirements.txt  

lint:
	pylint --disable=R,C compare_dataframes

test:
	python3 -m pytest -vv --cov=compare_dataframes compare_dataframes

