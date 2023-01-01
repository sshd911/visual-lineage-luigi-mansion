# https://github.com/sshd911/visual-lineage-pacman
push:
	git add .
	git commit -m 'fix'
	git push origin HEAD

# dev commands
run:
	open -na "Google Chrome" http://127.0.0.1:80
	flask run -h 0.0.0.0 -p 80
format: 
	black . --line-length=1000
	flake8
env:
	pipreqs --force 

# installation
install:
	pip install -r requirements.txt
	FLASK_APP=app.py
