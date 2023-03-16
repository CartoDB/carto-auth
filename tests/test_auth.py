import pytest
import pathlib

from datetime import datetime, timedelta

from carto_auth import CartoAuth, CredentialsError

HERE = pathlib.Path(__file__).parent


def test_from_oauth__not_use_cache(mocker):
    expiration = int((datetime.utcnow() + timedelta(seconds=10)).timestamp())
    load_mock = mocker.patch("carto_auth.auth.load_cache_file")
    save_mock = mocker.patch("carto_auth.auth.save_cache_file")
    get_oauth = mocker.patch(
        "carto_auth.auth.get_oauth_token_info",
        return_value={
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "expiration": expiration,
        },
    )
    get_api_base_url = mocker.patch(
        "carto_auth.auth.get_api_base_url",
        return_value="https://gcp-us-east1.api.carto.com",
    )

    carto_auth = CartoAuth.from_oauth(open_browser=False, use_cache=False)
    assert carto_auth._mode == "oauth"
    assert carto_auth._api_base_url == "https://gcp-us-east1.api.carto.com"
    assert str(carto_auth._cache_filepath).endswith(".carto-auth/token_oauth.json")
    assert carto_auth._use_cache is False
    assert carto_auth._access_token == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    assert carto_auth._expiration == expiration
    assert carto_auth._open_browser is False
    load_mock.assert_not_called()
    save_mock.assert_not_called()
    get_oauth.assert_called_once()
    get_api_base_url.assert_called_once()


def test_from_oauth__use_cache(mocker):
    expiration = int((datetime.utcnow() + timedelta(seconds=10)).timestamp())
    load_mock = mocker.patch(
        "carto_auth.auth.load_cache_file",
        return_value={
            "api_base_url": "https://gcp-us-east1.api.carto.com",
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "expiration": expiration,
        },
    )
    save_mock = mocker.patch("carto_auth.auth.save_cache_file")
    get_oauth = mocker.patch("carto_auth.auth.get_oauth_token_info")
    get_api_base_url = mocker.patch("carto_auth.auth.get_api_base_url")

    carto_auth = CartoAuth.from_oauth(open_browser=False, use_cache=True)
    assert carto_auth._mode == "oauth"
    assert carto_auth._api_base_url == "https://gcp-us-east1.api.carto.com"
    assert str(carto_auth._cache_filepath).endswith(".carto-auth/token_oauth.json")
    assert carto_auth._use_cache is True
    assert carto_auth._access_token == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    assert carto_auth._expiration == expiration
    assert carto_auth._open_browser is False
    load_mock.assert_called_once()
    save_mock.assert_called_once()
    get_oauth.assert_not_called()
    get_api_base_url.assert_not_called()


def test_from_oauth__use_cache_expired(mocker):
    expiration = int((datetime.utcnow() - timedelta(seconds=10)).timestamp())
    load_mock = mocker.patch(
        "carto_auth.auth.load_cache_file",
        return_value={
            "api_base_url": "https://gcp-us-east1.api.carto.com",
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "expiration": expiration,  # token expired
        },
    )
    save_mock = mocker.patch("carto_auth.auth.save_cache_file")
    expiration = int((datetime.utcnow() + timedelta(seconds=10)).timestamp())
    get_oauth = mocker.patch(
        "carto_auth.auth.get_oauth_token_info",
        return_value={
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "expiration": expiration,  # new token expiration
        },
    )
    get_api_base_url = mocker.patch(
        "carto_auth.auth.get_api_base_url",
        return_value="https://gcp-us-east1.api.carto.com",
    )

    carto_auth = CartoAuth.from_oauth(open_browser=False, use_cache=True)
    assert carto_auth._mode == "oauth"
    assert carto_auth._api_base_url == "https://gcp-us-east1.api.carto.com"
    assert str(carto_auth._cache_filepath).endswith(".carto-auth/token_oauth.json")
    assert carto_auth._use_cache is True
    assert carto_auth._access_token == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    assert carto_auth._expiration == expiration
    assert carto_auth._open_browser is False
    load_mock.assert_called_once()
    save_mock.assert_called_once()
    get_oauth.assert_called_once()
    get_api_base_url.assert_called_once()

def test_from_m2m_token__not_use_cache(mocker):
    expiration = int((datetime.utcnow() + timedelta(seconds=10)).timestamp())
    load_mock = mocker.patch("carto_auth.auth.load_cache_file")
    save_mock = mocker.patch("carto_auth.auth.save_cache_file")
    get_m2m = mocker.patch(
        "carto_auth.auth.get_m2m_token_info",
        return_value={
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "expiration": expiration,
        },
    )

    api_base_url = "https://gcp-us-east1.api.carto.com"
    client_id = "1234"
    client_secret = "1234567890"

    carto_auth = CartoAuth.from_m2m_token(api_base_url, client_id, client_secret, use_cache=False)
    assert carto_auth._mode == "m2m"
    assert carto_auth._api_base_url == api_base_url
    assert str(carto_auth._cache_filepath).endswith(".carto-auth/token_m2m.json")
    assert carto_auth._use_cache is False
    assert carto_auth._access_token == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    assert carto_auth._expiration == expiration
    assert carto_auth._client_id == client_id
    assert carto_auth._client_secret == client_secret
    load_mock.assert_not_called()
    save_mock.assert_not_called()
    get_m2m.assert_called_once()


def test_from_m2m_token__use_cache(mocker):
    expiration = int((datetime.utcnow() + timedelta(seconds=10)).timestamp())
    load_mock = mocker.patch(
        "carto_auth.auth.load_cache_file",
        return_value={
            "api_base_url": "https://gcp-us-east1.api.carto.com",
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "expiration": expiration,
        },
    )
    save_mock = mocker.patch("carto_auth.auth.save_cache_file")
    get_m2m = mocker.patch("carto_auth.auth.get_m2m_token_info")

    api_base_url = "https://gcp-us-east1.api.carto.com"
    client_id = "1234"
    client_secret = "1234567890"

    carto_auth = CartoAuth.from_m2m_token(api_base_url, client_id, client_secret, use_cache=True)
    assert carto_auth._mode == "m2m"
    assert carto_auth._api_base_url == api_base_url
    assert str(carto_auth._cache_filepath).endswith(".carto-auth/token_m2m.json")
    assert carto_auth._use_cache is True
    assert carto_auth._access_token == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    assert carto_auth._expiration == expiration
    assert carto_auth._client_id == client_id
    assert carto_auth._client_secret == client_secret
    load_mock.assert_called_once()
    save_mock.assert_called_once()
    get_m2m.assert_not_called()


def test_from_m2m_token__use_cache_expired(mocker):
    expiration = int((datetime.utcnow() - timedelta(seconds=10)).timestamp())
    load_mock = mocker.patch(
        "carto_auth.auth.load_cache_file",
        return_value={
            "api_base_url": "https://gcp-us-east1.api.carto.com",
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "expiration": expiration,  # token expired
        },
    )
    save_mock = mocker.patch("carto_auth.auth.save_cache_file")
    expiration = int((datetime.utcnow() + timedelta(seconds=10)).timestamp())
    get_m2m = mocker.patch(
        "carto_auth.auth.get_m2m_token_info",
        return_value={
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "expiration": expiration,  # new token expiration
        },
    )

    api_base_url = "https://gcp-us-east1.api.carto.com"
    client_id = "1234"
    client_secret = "1234567890"

    carto_auth = CartoAuth.from_m2m_token(api_base_url, client_id, client_secret, use_cache=True)
    assert carto_auth._mode == "m2m"
    assert carto_auth._api_base_url == api_base_url
    assert str(carto_auth._cache_filepath).endswith(".carto-auth/token_m2m.json")
    assert carto_auth._use_cache is True
    assert carto_auth._access_token == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    assert carto_auth._expiration == expiration
    assert carto_auth._client_id == client_id
    assert carto_auth._client_secret == client_secret
    load_mock.assert_called_once()
    save_mock.assert_called_once()
    get_m2m.assert_called_once()

def test_from_m2m_token_error():
    api_base_url = "https://gcp-us-east1.api.carto.com"
    client_id = "1234"
    client_secret = "1234567890"

    with pytest.raises(ValueError):
        CartoAuth.from_m2m_token(None, client_id, client_secret)

    with pytest.raises(ValueError):
        CartoAuth.from_m2m_token(api_base_url, None, client_secret)

    with pytest.raises(ValueError):
        CartoAuth.from_m2m_token(api_base_url, client_id, None)

def test_from_m2m__not_use_cache(mocker):
    expiration = int((datetime.utcnow() + timedelta(seconds=10)).timestamp())
    load_mock = mocker.patch("carto_auth.auth.load_cache_file")
    save_mock = mocker.patch("carto_auth.auth.save_cache_file")
    get_m2m = mocker.patch(
        "carto_auth.auth.get_m2m_token_info",
        return_value={
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "expiration": expiration,
        },
    )

    filepath = HERE / "fixtures/carto_credentials_ok.json"
    carto_auth = CartoAuth.from_m2m(filepath, use_cache=False)
    assert carto_auth._mode == "m2m"
    assert carto_auth._api_base_url == "https://gcp-us-east1.api.carto.com"
    assert str(carto_auth._cache_filepath).endswith(".carto-auth/token_m2m.json")
    assert carto_auth._use_cache is False
    assert carto_auth._access_token == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    assert carto_auth._expiration == expiration
    assert carto_auth._client_id == "1234"
    assert carto_auth._client_secret == "1234567890"
    load_mock.assert_not_called()
    save_mock.assert_not_called()
    get_m2m.assert_called_once()


def test_from_m2m__use_cache(mocker):
    expiration = int((datetime.utcnow() + timedelta(seconds=10)).timestamp())
    load_mock = mocker.patch(
        "carto_auth.auth.load_cache_file",
        return_value={
            "api_base_url": "https://gcp-us-east1.api.carto.com",
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "expiration": expiration,
        },
    )
    save_mock = mocker.patch("carto_auth.auth.save_cache_file")
    get_m2m = mocker.patch("carto_auth.auth.get_m2m_token_info")

    filepath = HERE / "fixtures/carto_credentials_ok.json"
    carto_auth = CartoAuth.from_m2m(filepath, use_cache=True)
    assert carto_auth._mode == "m2m"
    assert carto_auth._api_base_url == "https://gcp-us-east1.api.carto.com"
    assert str(carto_auth._cache_filepath).endswith(".carto-auth/token_m2m.json")
    assert carto_auth._use_cache is True
    assert carto_auth._access_token == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    assert carto_auth._expiration == expiration
    assert carto_auth._client_id == "1234"
    assert carto_auth._client_secret == "1234567890"
    load_mock.assert_called_once()
    save_mock.assert_called_once()
    get_m2m.assert_not_called()


def test_from_m2m__use_cache_expired(mocker):
    expiration = int((datetime.utcnow() - timedelta(seconds=10)).timestamp())
    load_mock = mocker.patch(
        "carto_auth.auth.load_cache_file",
        return_value={
            "api_base_url": "https://gcp-us-east1.api.carto.com",
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "expiration": expiration,  # token expired
        },
    )
    save_mock = mocker.patch("carto_auth.auth.save_cache_file")
    expiration = int((datetime.utcnow() + timedelta(seconds=10)).timestamp())
    get_m2m = mocker.patch(
        "carto_auth.auth.get_m2m_token_info",
        return_value={
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "expiration": expiration,  # new token expiration
        },
    )

    filepath = HERE / "fixtures/carto_credentials_ok.json"
    carto_auth = CartoAuth.from_m2m(filepath, use_cache=True)
    assert carto_auth._mode == "m2m"
    assert carto_auth._api_base_url == "https://gcp-us-east1.api.carto.com"
    assert str(carto_auth._cache_filepath).endswith(".carto-auth/token_m2m.json")
    assert carto_auth._use_cache is True
    assert carto_auth._access_token == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    assert carto_auth._expiration == expiration
    assert carto_auth._client_id == "1234"
    assert carto_auth._client_secret == "1234567890"
    load_mock.assert_called_once()
    save_mock.assert_called_once()
    get_m2m.assert_called_once()


def test_from_m2m_error():
    filepath = HERE / "fixtures/carto_credentials_no_attr.json"
    with pytest.raises(AttributeError):
        CartoAuth.from_m2m(filepath)

    filepath = HERE / "fixtures/carto_credentials_no_value.json"
    with pytest.raises(ValueError):
        CartoAuth.from_m2m(filepath)


def test_get_api_base_url(mocker):
    save_mock = mocker.patch("carto_auth.auth.save_cache_file")

    carto_auth = CartoAuth("oauth", api_base_url="https://gcp-us-east1.api.carto.com")

    api_base_url = carto_auth.get_api_base_url()

    assert api_base_url == "https://gcp-us-east1.api.carto.com"
    save_mock.assert_not_called()


def test_get_access_token(mocker):
    save_mock = mocker.patch("carto_auth.auth.save_cache_file")

    access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    expiration = int((datetime.utcnow() + timedelta(seconds=10)).timestamp())
    carto_auth = CartoAuth("oauth", access_token=access_token, expiration=expiration)

    access_token = carto_auth.get_access_token()

    assert access_token == access_token
    assert carto_auth._access_token == access_token
    assert carto_auth._expiration == expiration
    save_mock.assert_not_called()


def test_get_access_token_oauth_expired(mocker):
    new_expiration = int((datetime.utcnow() + timedelta(seconds=10)).timestamp())
    get_oauth = mocker.patch(
        "carto_auth.auth.get_oauth_token_info",
        return_value={
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "expiration": new_expiration,
        },
    )

    access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    expiration = int((datetime.utcnow() - timedelta(seconds=10)).timestamp())
    carto_auth = CartoAuth("oauth", access_token=access_token, expiration=expiration)

    access_token = carto_auth.get_access_token()

    assert access_token == access_token
    assert carto_auth._access_token == access_token
    assert carto_auth._expiration == new_expiration
    get_oauth.assert_called_once()


def test_get_access_token_m2m_expired(mocker):
    new_expiration = int((datetime.utcnow() + timedelta(seconds=10)).timestamp())
    get_m2m = mocker.patch(
        "carto_auth.auth.get_m2m_token_info",
        return_value={
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "expiration": new_expiration,
        },
    )

    access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    expiration = int((datetime.utcnow() - timedelta(seconds=10)).timestamp())
    carto_auth = CartoAuth("m2m", access_token=access_token, expiration=expiration)

    access_token = carto_auth.get_access_token()

    assert access_token == access_token
    assert carto_auth._access_token == access_token
    assert carto_auth._expiration == new_expiration
    get_m2m.assert_called_once()


def test_carto_dw_credentials(mocker, requests_mock):
    mocker.patch(
        "carto_auth.auth.CartoAuth.get_access_token",
        return_value="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
    )
    requests_mock.get(
        "https://gcp-us-east1.api.carto.com/v3/connections/carto-dw/token",
        json={
            "projectId": "project-id-mock",
            "token": "token-mock",
        },
    )

    api_base_url = "https://gcp-us-east1.api.carto.com"
    access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    expiration = int((datetime.utcnow() + timedelta(seconds=10)).timestamp())
    carto_auth = CartoAuth(
        "oauth",
        api_base_url=api_base_url,
        access_token=access_token,
        expiration=expiration,
    )

    carto_dw_project_id, carto_dw_token = carto_auth.get_carto_dw_credentials()

    assert carto_dw_project_id == "project-id-mock"
    assert carto_dw_token == "token-mock"


def test_carto_dw_credentials_error(mocker, requests_mock):
    mocker.patch(
        "carto_auth.auth.CartoAuth.get_access_token",
        return_value="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
    )
    requests_mock.get(
        "https://gcp-us-east1.api.carto.com/v3/connections/carto-dw/token",
        text="wrong json",
    )

    api_base_url = "https://gcp-us-east1.api.carto.com"
    access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    expiration = int((datetime.utcnow() + timedelta(seconds=10)).timestamp())
    carto_auth = CartoAuth(
        "oauth",
        api_base_url=api_base_url,
        access_token=access_token,
        expiration=expiration,
    )

    with pytest.raises(CredentialsError):
        carto_auth.get_carto_dw_credentials()

    requests_mock.get(
        "https://gcp-us-east1.api.carto.com/v3/connections/carto-dw/token",
        json={
            "token": "token-mock",
        },
    )
    with pytest.raises(CredentialsError):
        carto_auth.get_carto_dw_credentials()

    requests_mock.get(
        "https://gcp-us-east1.api.carto.com/v3/connections/carto-dw/token",
        json={
            "projectId": "project-id-mock",
            "token": "token-mock",
        },
    )
    carto_auth = CartoAuth("oauth", access_token=access_token, expiration=expiration)
    with pytest.raises(CredentialsError):
        carto_auth.get_carto_dw_credentials()


def test_carto_dw_client(mocker):
    from google.cloud.bigquery import Client

    get_creds = mocker.patch(
        "carto_auth.auth.CartoAuth.get_carto_dw_credentials",
        return_value=("project-id-mock", "token-mock"),
    )

    api_base_url = "https://gcp-us-east1.api.carto.com"
    access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"
    expiration = int((datetime.utcnow() + timedelta(seconds=10)).timestamp())
    carto_auth = CartoAuth(
        "oauth",
        api_base_url=api_base_url,
        access_token=access_token,
        expiration=expiration,
    )

    bq_client = carto_auth.get_carto_dw_client()
    assert isinstance(bq_client, Client)
    assert bq_client.project == "project-id-mock"
    get_creds.assert_called_once()
