all:

.PHONY: clean
clean:
	rm -rf build *.egg-info dist

.PHONY: install
install:
	sudo python3.5 setup.py install

.PHONY: uninstall
uninstall:
	sudo python3.5 -m pip uninstall kilroy -y

.PHONY: test
test:
	python3 -m unittest discover tests
