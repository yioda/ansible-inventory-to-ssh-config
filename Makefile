# Parser each playbooks with `*.yml`, and no include `requirements*.yml`.
#PLAYBOOKS = $(shell ls *.yml | sed '/requirements/d')

main: build

# ---- Initialization ----------------------------------------------------------

build: clean
	python setup.py sdist bdist_wheel

push_test:
	python3 -m twine upload --repository testpypi dist/*

push_prod:
	python3 -m twine upload dist/*

clean:
	rm -rf build/ *.egg-info/ dist/