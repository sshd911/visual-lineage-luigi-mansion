push:
	git add .
	git commit -m 'fix'
	git push origin HEAD
run:
	open -na "Google Chrome" http://127.0.0.1:80
	FLASK_APP=app.py FLASK_DEBUG=1 flask run --host=0.0.0.0 --port=80
env:
	pipreqs --force 
format: 
	black . --line-length=1000
	.flake8
install:
	pip install -r requirements.txt
