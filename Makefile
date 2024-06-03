# Parser each playbooks with `*.yml`, and no include `requirements*.yml`.
#PLAYBOOKS = $(shell ls *.yml | sed '/requirements/d')
PY_FILES = $(shell git ls-files '*.py')

main: build

lint_check:
	pylint --disable C0114,C0115,C0116 $(PY_FILES)

build: clean
	pip install --upgrade build
	python -m build

push_test:
	python3 -m twine upload --repository testpypi dist/*

push_prod:
	python3 -m twine upload dist/*

clean:
	rm -rf build/ *.egg-info/ dist/
