# https://github.com/sshd911/visual-lineage-packman
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
write_env:
	pipreqs --force 
prod_mode:
	export FLASK_ENV=production
dev_mode:
	export FLASK_ENV=development

# npm scripts
build:
	npm run build
watch:
	npm run watch

# installation
install:
	pip install -r requirements.txt
	FLASK_APP=app.py
	FLASK_DEBUG=1 
	npm install && npm run build
