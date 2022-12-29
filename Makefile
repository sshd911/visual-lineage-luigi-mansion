format: 
	black .
run:
	open http://localhost:8080
	python app.py
push:
	git add .
	git commit -m 'fix'
	git push origin HEAD