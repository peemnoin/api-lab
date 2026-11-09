# A new rating comes back with an id, its stars and its pizza.
def test_create_rating(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 5}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201
    body = res.json()
    assert body["stars"] == 5
    assert body["pizza_id"] == pizza_id
    assert isinstance(body["id"], int)
