import pytest


# The pizza never needs a tool that the customer excluded.
@pytest.mark.parametrize("excluded", [["Knife"], ["Scissors"]])
def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded
