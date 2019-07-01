init:
	sudo apt-get install python3 nodejs
	pip3 --no-cache-dir install -r requirements.txt
	npm install --prefix phantom/database/js
	sudo chmod 770 build.sh

test:
	py.test tests

.PHONY: 
	init test
