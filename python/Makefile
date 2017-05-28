all:

.PHONY: clean
clean:
	rm -rf build *.egg-info dist

.PHONY: install
install:
	sudo python3.5 setup.py install

.PHONY: uninstall
uninstall:
	sudo pip3 uninstall -y kilroy

.PHONY: test
test:
	python3 -m unittest discover tests
