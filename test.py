from fastapi.testclient import TestClient

def test_client():
    assert type(client) == TestClient

