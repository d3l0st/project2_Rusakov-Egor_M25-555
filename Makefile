install:
	poetry install
database:
	poetry run database
build:
	poetry build
publish:
	poetry publish --dry-run
package-install:
	python3 -m pip install dist/*.whl
init:
	poetry run ruff check .
 