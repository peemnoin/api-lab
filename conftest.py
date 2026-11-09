import uuid

import pytest
import requests

SITE = "https://quickpizza.grafana.com"


class QuickPizza(requests.Session):
    """A session that puts the address of the site in front of each path."""

    def request(self, method, url, *args, **kwargs):
        return super().request(method, SITE + url, *args, **kwargs)


@pytest.fixture(scope="session")
def api():
    with QuickPizza() as session:
        yield session
