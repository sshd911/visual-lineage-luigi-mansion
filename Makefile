push:
	git add .
	git commit -m 'fix'
	git push origin HEAD
run:
	open -na "Google Chrome" http://localhost:80
	python src/app.py
env:
	pipreqs --force 
format: 
	black .
check:
	flake8
install:
	pip install -r requirements.txt
