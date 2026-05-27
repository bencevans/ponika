setup:
	uv venv --python 3.14
	uv sync --group dev

checkformat:
	.venv/bin/ruff check

format:
	.venv/bin/ruff format
	
test:
	.venv/bin/pytest -m unit

