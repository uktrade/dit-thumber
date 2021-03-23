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
	pip install wheel; \
	python setup.py bdist_wheel; \
	twine upload --username $$DIRECTORY_PYPI_USERNAME --password $$DIRECTORY_PYPI_PASSWORD dist/*

.PHONY: clean test_requirements publish test