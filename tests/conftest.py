import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_mod


@pytest.fixture
def client():
    """Provide a TestClient and restore global state after each test.

    Uses deep copy to snapshot `app_mod.activities` and restores it in teardown
    so tests remain isolated.
    """
    original = copy.deepcopy(app_mod.activities)
    with TestClient(app_mod.app) as client:
        yield client
    app_mod.activities.clear()
    app_mod.activities.update(original)
