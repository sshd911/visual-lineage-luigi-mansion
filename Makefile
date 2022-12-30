push:
	git add .
	git commit -m 'fix'
	git push origin HEAD
run:
	open http://localhost:8080
	python app.py
env:
	pipreqs --force 
format: 
	black .
install:
	pip install -r requirements.txt
