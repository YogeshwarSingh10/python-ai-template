format:
	ruff format .

lint:
	ruff check .

typecheck:
	pyright

test:
	pytest

check:
	ruff check .
	pyright
	pytest