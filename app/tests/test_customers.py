from fastapi import status

# tests/test_customers.py -v

def test_create_customer(client):
    payload = {"name": "John Doe", "email": "john@exe.com", "age": 30}
    r = client.post("/customers", json=payload)
    assert r.status_code == status.HTTP_201_CREATED
    body = r.json()
    assert body["id"] > 0
    assert body["name"] == payload["name"]
    assert body["email"] == payload["email"]
    assert body["age"] == payload["age"]

def test_read_customer(client):
    payload = {"name": "Jane", "email": "jane@exe.com", "age": 28}
    created = client.post("/customers", json=payload)
    assert created.status_code == status.HTTP_201_CREATED
    cid = created.json()["id"]

    got = client.get(f"/customers/{cid}")
    assert got.status_code == status.HTTP_200_OK
    assert got.json()["name"] == payload["name"]

def test_update_customer(client):
    created = client.post("/customers", json={"name": "D", "email": "d@x.com", "age": 23})
    cid = created.json()["id"]

    upd = client.patch(f"/customers/{cid}", json={"age": 24, "description": "VIP"})
    assert upd.status_code == status.HTTP_200_OK
    body = upd.json()
    assert body["age"] == 24
    assert body["description"] == "VIP"

def test_delete_customer(client):
    created = client.post("/customers", json={"name": "E", "email": "e@x.com", "age": 25})
    cid = created.json()["id"]

    r = client.delete(f"/customers/{cid}")
    assert r.status_code == status.HTTP_204_NO_CONTENT

    r2 = client.get(f"/customers/{cid}")
    assert r2.status_code == status.HTTP_404_NOT_FOUND

def test_list_customers(client):
    client.post("/customers", json={"name": "A", "email": "a@x.com", "age": 20})
    client.post("/customers", json={"name": "B", "email": "b@x.com", "age": 21})
    r = client.get("/customers")
    assert r.status_code == status.HTTP_200_OK
    items = r.json()
    assert isinstance(items, list)
    assert len(items) >= 2
