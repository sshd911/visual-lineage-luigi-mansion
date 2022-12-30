push:
	git add .
	git commit -m 'fix'
	git push origin HEAD
run:
	open http://localhost:8080
	python -B src/app.py
env:
	pipreqs --force 
format: 
	black .
check:
	flake8
install:
	pip install -r requirements.txt
