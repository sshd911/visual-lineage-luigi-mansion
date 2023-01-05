#!make

BROWSER='Google Chrome'
HOST=127.0.0.1
PORT=80

# Develop Command
run:
	open -na $(BROWSER) http://${HOST}:${PORT}
	sudo FLASK_APP=app.py FLASK_DEBUG=1 flask run -h ${HOST} -p ${PORT}
format: 
	black . --line-length=1000
	flake8
env:
	pipreqs --force 

# Installation Commands
install:
	pip install -r requirements.txt
