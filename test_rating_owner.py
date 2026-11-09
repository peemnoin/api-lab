# Another user may not read, change or delete a rating. Each attempt is refused
# with a 4xx status, and the owner then reads the rating unchanged.


def assert_unchanged(api, auth, rating):
    """The owner reads the rating and finds the same fields as before."""
    res = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert res.status_code == 200
    assert res.json() == rating


# Another user cannot read the rating of the owner.
def test_other_user_cannot_read(api, auth, other_auth, rating):
    res = api.get(f"/api/ratings/{rating['id']}", headers=other_auth)
    assert 400 <= res.status_code <= 499
    assert "stars" not in res.json()
    assert_unchanged(api, auth, rating)


# Another user cannot change the stars of the rating of the owner.
def test_other_user_cannot_change(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": 1}, headers=other_auth)
    assert 400 <= res.status_code <= 499
    assert_unchanged(api, auth, rating)


# Another user cannot delete the rating of the owner.
def test_other_user_cannot_delete(api, auth, other_auth, rating):
    res = api.delete(f"/api/ratings/{rating['id']}", headers=other_auth)
    assert 400 <= res.status_code <= 499
    assert_unchanged(api, auth, rating)
