import requests
from unittest.mock import Mock

from src.fetcher import fetch_page

def test_fetch_page_returns_http_error(monkeypatch):
    fake_response = Mock()
    fake_response.status_code = 404
    fake_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "404 Client Error",
        response=fake_response
    )
    monkeypatch.setattr(
        "src.fetcher.requests.get",
        lambda *args, **kwargs: fake_response,
    )

    response = fetch_page("https://example.com")
    assert response["status_code"] == 404
    assert response["error_type"] == "http_error"
    assert response["html"] is None
    assert "404" in response["error"]