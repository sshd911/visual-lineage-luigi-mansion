format: 
	black .
run:
	python app.py
push:
	git add .
	git commit -m 'fix'
	git push origin HEAD
