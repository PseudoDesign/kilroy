all:

.PHONY: clean
clean:
	rm -rf build *.egg-info dist

.PHONY: install
install:
	sudo python3.5 setup.py install

.PHONY: uninstall
uninstall:
	sudo rm -r /usr/local/lib/python3.5/dist-packages/kilroy*

.PHONY: test
test:
	python3 -m unittest discover tests
