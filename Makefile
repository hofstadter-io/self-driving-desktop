
.PHONY: build
build:
	python setup.py sdist

.PHONY: upload
upload:
	twine upload dist/self-driving-desktop-*.tar.gz

.PHONY: upload-test
upload-test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/self-driving-desktop-*.tar.gz

.PHONY: clean
clean:
	rm -rf dist build self_driving_desktop.egg-info
