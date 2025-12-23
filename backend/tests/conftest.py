import os

import pytest

from app.services.store import store

# Ensure the JSON store stays in-memory during automated tests
os.environ.setdefault("STORE_PATH", ":memory:")


@pytest.fixture(autouse=True)
def reset_store():
	"""Guarantee every test starts with a clean store."""
	store.clear()
	yield
	store.clear()
