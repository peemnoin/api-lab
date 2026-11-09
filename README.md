# api-lab

API tests for [QuickPizza](https://quickpizza.grafana.com) with pytest and requests
(ITCS386 Software Verification and Validation, Lab: API Testing with pytest and requests).

## Install and run

Python 3.10 or newer is needed.

macOS and Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest -v
```

Save the output of a full run as an HTML report:

```bash
pytest -v --html=report.html --self-contained-html
```

A full run sends about 140 requests to the shared QuickPizza site and takes under a
minute. Every test that changes data creates its own user with a new name (fixtures in
`conftest.py`), so no test uses the public token to create or change ratings.

## Files

| File | What it tests |
|------|---------------|
| `conftest.py` | Fixtures: one session for the run (`api`), a new logged-in user (`auth`, `other_auth`), a new pizza (`pizza_id`), and a rating that is deleted after the test (`rating`) |
| `test_names.py` | `GET /api/names` |
| `test_tools.py` | `GET /api/tools` with the public token |
| `test_pizza.py` | `POST /api/pizza`, vegetarian pizza and refusal without token |
| `test_users.py` | A new user starts with no ratings |
| `test_ratings.py` | Create, read, update and delete a rating |
| `test_refused.py` | Taken user name, wrong password, empty user name |
| `test_excluded_tools.py` | `excludedTools`, one input per block, and Defect 1 (xfail) |
| `test_create_rating.py` | `POST /api/ratings`, base choice coverage of the model below |
| `test_update_rating.py` | `PUT /api/ratings/{id}`, boundary values of `stars` |
| `test_rating_owner.py` | Another user may not read, change or delete a rating |

## Input domain model for `POST /api/ratings`

The operation takes a body with two fields, `pizza_id` and `stars`, and a token in the
`Authorization` header. QuickPizza accepts a whole number of stars from 1 to 5, a pizza
that exists, and the token of a logged-in user. Each characteristic below comes from one
of these rules. The blocks of each characteristic do not overlap and together cover
every value. The base block of each characteristic is the most common valid value.

| Characteristic | Blocks | Values in the tests |
|----------------|--------|---------------------|
| C1 Value of `stars` | below 1, 1 to 5 (base), above 5 | 0, 3, 6 |
| C2 Type of `stars` | whole number (base), decimal, text, missing | 3, 3.5, "3", no field |
| C3 Pizza | exists (base), does not exist | a new pizza, 999999999 |
| C4 Token | the user's own (base), none, wrong length | from `auth`, no header, `token short` |

### Test that covers each block (base choice coverage)

The base test uses every base block. Every other test changes one characteristic to
one of its other blocks and keeps the rest at the base. All tests are in
`test_create_rating.py`.

| Characteristic | Block | Test |
|----------------|-------|------|
| C1 | below 1 | `test_stars_out_of_range[0]` |
| C1 | 1 to 5 (base) | `test_base_choice_is_saved` |
| C1 | above 5 | `test_stars_out_of_range[6]` |
| C2 | whole number (base) | `test_base_choice_is_saved` |
| C2 | decimal | `test_decimal_stars_is_refused` |
| C2 | text | `test_text_stars_is_refused` |
| C2 | missing | `test_missing_stars_is_refused` |
| C3 | exists (base) | `test_base_choice_is_saved` |
| C3 | does not exist | `test_unknown_pizza_is_refused` |
| C4 | the user's own (base) | `test_base_choice_is_saved` |
| C4 | none | `test_no_token_is_refused` |
| C4 | wrong length | `test_short_token_is_refused` |

Base choice coverage needs 1 + (3−1) + (4−1) + (2−1) + (3−1) = 1 + 2 + 3 + 1 + 2 = **9 tests**.
All combinations coverage would need 3 × 4 × 2 × 3 = **72 tests**.

### Boundary values for `PUT /api/ratings/{id}`

The rule "1 to 5 stars" has two edges, so `test_update_rating.py` tests the value on
each side of both edges: 0 and 6 must be refused with 400 and leave the rating at 3
stars, while 1 and 5 must be saved with 200.
