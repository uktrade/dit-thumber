ARGUMENTS = $(filter-out $@,$(MAKECMDGOALS))

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

test:
	python run_tests.py

test_requirements:
	pip install -e .[test]


publish:
	rm -rf build dist; \
	python setup.py bdist_wheel; \
	twine upload --username '__token__' --password 'pypi-AgEIcHlwaS5vcmcCJDUzNzQ3ZTdiLWE2Y2YtNGMwYi05ZjIzLWNlZWJhZjM0NjI0MwACKlszLCIzNjBiODEyZi1hZWNmLTQ2ZDEtYjllMC0wM2U3NTdjMjVhMTgiXQAABiBB5_bL3Oconw1R2N-ug2_yrUtZpO8XHIJVd1dWQjkpeg' dist/*

.PHONY: clean test_requirements publish test