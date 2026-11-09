import pytest


# Changing stars to a boundary value: 1 and 5 are saved with 200, while 0 and 6
# are refused with 400 and leave the rating as it was.
@pytest.mark.parametrize("stars, status", [(0, 400), (1, 200), (5, 200), (6, 400)])
def test_update_stars_boundaries(api, auth, rating, stars, status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == status
    expected = stars if status == 200 else rating["stars"]
    res = api.get(path, headers=auth)
    assert res.status_code == 200
    assert res.json()["stars"] == expected
