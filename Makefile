install:
	poetry install

lint:
	poetry run flake8 metr/ tests/
	poetry run black --check --diff metr/ tests/
	poetry run isort --check-only metr/ tests/

format:
	poetry run isort metr/ tests/
	poetry run black metr/ tests/

test:
	poetry run mypy -p metr -p tests
	poetry run coverage run -m pytest --failed-first -vv
	poetry run coverage report
	poetry run coverage html
