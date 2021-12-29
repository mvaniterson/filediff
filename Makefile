install:
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt

lint:
	pylint --disable=R,C hello.py

test:
	python3 -m pytest -vv --cov=hello test_hello.py
	    
