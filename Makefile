.PHONY: setup dev test lint format smoke public-ready

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip
	. .venv/bin/activate && pip install -e ".[dev]"

dev:
	. .venv/bin/activate && uvicorn storms_agents.api.main:app --host 0.0.0.0 --port 8080 --reload

test:
	. .venv/bin/activate && pytest

lint:
	. .venv/bin/activate && ruff check src tests

format:
	. .venv/bin/activate && ruff format src tests

smoke:
	./scripts/smoke-test.sh

public-ready:
	./scripts/check-public-ready.sh
