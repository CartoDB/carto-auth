import pytest
import pathlib

from datetime import datetime, timedelta
from carto_auth.errors import CredentialsError
from carto_auth.utils import (
    get_cache_filepath,
    get_oauth_token_info,
    get_m2m_token_info,
    get_api_base_url,
    load_cache_file,
    save_cache_file,
    is_token_expired,
)

HERE = pathlib.Path(__file__).parent


def test_get_oauth_token_info(mocker, requests_mock):
    mocker.patch(
        "carto_auth.pkce.CartoPKCE._input",
        return_value="carto.com/autorize?code=abcde",
    )
    requests_mock.post(
        "https://auth.carto.com/oauth/token",
        json={
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "scope": "",
            "expires_in": 86400,
            "token_type": "Bearer",
        },
    )

    token_info = get_oauth_token_info(open_browser=False)

    assert token_info["access_token"] == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    assert token_info["expiration"] >= int(
        (datetime.utcnow() + timedelta(seconds=86400)).timestamp()
    )

    mocker.patch(
        "webbrowser.open_new",
        return_value=True,
    )

    token_info = get_oauth_token_info(open_browser=True)


def test_get_oauth_token_info_error(mocker, requests_mock):
    mocker.patch(
        "carto_auth.pkce.CartoPKCE._input",
        return_value="carto.com/autorize?code=abcde",
    )
    requests_mock.post(
        "https://auth.carto.com/oauth/token",
        text="{",
    )
    with pytest.raises(CredentialsError):
        get_oauth_token_info(open_browser=False)

    requests_mock.post(
        "https://auth.carto.com/oauth/token",
        json={},
    )
    with pytest.raises(CredentialsError):
        get_oauth_token_info(open_browser=False)


def test_get_m2m_token_info(requests_mock):
    requests_mock.post(
        "https://auth.carto.com/oauth/token",
        json={
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "scope": "",
            "expires_in": 86400,
            "token_type": "Bearer",
        },
    )

    token_info = get_m2m_token_info("1234", "1234567890")

    assert token_info["access_token"] == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    assert token_info["expiration"] >= int(
        (datetime.utcnow() + timedelta(seconds=86400)).timestamp()
    )


def test_get_m2m_token_info_error(requests_mock):
    requests_mock.post(
        "https://auth.carto.com/oauth/token",
        text="{",
    )
    with pytest.raises(CredentialsError):
        get_m2m_token_info("1234", "1234567890")

    requests_mock.post(
        "https://auth.carto.com/oauth/token",
        json={},
    )
    with pytest.raises(CredentialsError):
        get_m2m_token_info("1234", "1234567890")


def test_get_api_base_url(requests_mock):
    requests_mock.get(
        "https://accounts.app.carto.com/accounts",
        json={
            "tenant_domain": "clausa.app.carto.com",
        },
    )
    requests_mock.get(
        "https://clausa.app.carto.com/config.yaml",
        text="""
        apis:
            baseUrl: "https://gcp-us-east1.api.carto.com"
        """,
    )

    api_base_url = get_api_base_url("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX")

    assert api_base_url == "https://gcp-us-east1.api.carto.com"


def test_get_api_base_url_error(requests_mock):
    requests_mock.get(
        "https://accounts.app.carto.com/accounts",
        text="wrong json",
    )
    with pytest.raises(CredentialsError):
        get_api_base_url("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX")

    requests_mock.get(
        "https://accounts.app.carto.com/accounts",
        json={
            "tenant_domain": "clausa.app.carto.com",
        },
    )
    requests_mock.get(
        "https://clausa.app.carto.com/config.yaml",
        text="wrong yaml",
    )
    with pytest.raises(CredentialsError):
        get_api_base_url("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX")


def test_get_cache_filepath():
    filepath = get_cache_filepath("m2m")
    assert str(filepath).endswith(".carto-auth/token_m2m.json")


def test_load_cache_file():
    data = load_cache_file(HERE / "fixtures/token_ok.json")

    assert data["api_base_url"] == "https://gcp-us-east1.api.carto.com"
    assert data["access_token"] == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    assert data["expiration"] == 1667471700


def test_load_cache_file_none():
    data = load_cache_file(HERE / "fixtures/token_error.json")

    assert data is None

    data = load_cache_file(HERE / "__token__.json")

    assert data is None


def test_save_cache_file(tmp_path):
    data = {
        "api_base_url": "https://gcp-us-east1.api.carto.com",
        "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
        "expiration": 1667471700,
    }

    save_cache_file(tmp_path / "carto_token_saved.json", data)
    data = load_cache_file(tmp_path / "carto_token_saved.json")

    assert data["api_base_url"] == "https://gcp-us-east1.api.carto.com"
    assert data["access_token"] == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    assert data["expiration"] == 1667471700


def test_is_token_expired():
    now = datetime.utcnow()
    assert is_token_expired(None) is True
    assert is_token_expired(0) is True
    assert is_token_expired(1) is True
    assert is_token_expired((now - timedelta(seconds=10)).timestamp()) is True
    assert is_token_expired((now + timedelta(seconds=10)).timestamp()) is False
