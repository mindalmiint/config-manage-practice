.PHONY: test run clean

test:
	pytest tests/ -v

run:
	python3 src/main.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache