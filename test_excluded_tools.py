import pytest


# The pizza never needs a tool that the customer excluded.
# One input per block of "how many of the three tools are excluded":
# none, one (two inputs), two. The block "all three" has its own test below.
@pytest.mark.parametrize("excluded", [
    [],
    ["Knife"],
    ["Scissors"],
    ["Knife", "Scissors"],
])
def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# Excluding all three tools leaves no pizza that can be cut, so the request
# is refused with 400 and a JSON error message, never a 500.
@pytest.mark.xfail(
    reason="Defect 1: excluding all three tools returns 500 with an empty body "
    "instead of 400 with a JSON error message",
    strict=True,
)
def test_all_tools_excluded_is_refused(api, auth):
    body = {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()
