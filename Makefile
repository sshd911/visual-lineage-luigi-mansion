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

# settings for apple silicon
settings:
	brew install protobuf
	brew install Bazel
	git clone https://github.com/cansik/mediapipe-silicon.git && cd mediapipe-silicon
	./build-macos.sh
	cd dist
	pip install mediapipe_silicon-0.8.10.1-cp38-cp38-macosx_11_0_arm64.whl