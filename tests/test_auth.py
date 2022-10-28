import os
import pytest
import datetime


from carto_auth import CartoAuth, CredentialsError


def test_carto_auth_from_parameters(requests_mock):
    requests_mock.post(
        "https://auth.carto.com/oauth/token",
        json={
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "scope": "",
            "expires_in": 86400,
            "token_type": "Bearer",
        },
    )

    carto_auth = CartoAuth(
        client_id="1234", client_secret="1234567890", use_cache=False
    )
    assert carto_auth.client_id == "1234"
    assert carto_auth.client_secret == "1234567890"
    assert carto_auth.api_base_url == "https://gcp-us-east1.api.carto.com"
    assert str(carto_auth.cache_filepath).endswith(".carto-auth/token.json")

    access_token = carto_auth.get_access_token()
    assert access_token == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"


def test_carto_auth_from_file(requests_mock):
    requests_mock.post(
        "https://auth.carto.com/oauth/token",
        json={
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "scope": "",
            "expires_in": 86400,
            "token_type": "Bearer",
        },
    )

    filepath = "fixtures/carto_credentials_ok.json"
    fullpath = os.path.join(os.path.dirname(__file__), filepath)
    carto_auth = CartoAuth.from_file(filepath=fullpath, use_cache=False)
    assert carto_auth.client_id == "1234"
    assert carto_auth.client_secret == "1234567890"
    assert carto_auth.api_base_url == "https://api.carto.com"
    assert carto_auth._token_expired() is True
    assert str(carto_auth.cache_filepath).endswith(".carto-auth/token.json")

    access_token = carto_auth.get_access_token()
    assert access_token == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"

    current_utc_ts = datetime.datetime.utcnow().timestamp()
    assert carto_auth._expiration_ts > current_utc_ts
    assert carto_auth._token_expired() is False

    filepath = "fixtures/carto_credentials_no_attr.json"
    fullpath = os.path.join(os.path.dirname(__file__), filepath)
    with pytest.raises(AttributeError):
        CartoAuth.from_file(filepath=fullpath, use_cache=False)

    filepath = "fixtures/carto_credentials_no_value.json"
    fullpath = os.path.join(os.path.dirname(__file__), filepath)
    with pytest.raises(ValueError):
        CartoAuth.from_file(filepath=fullpath, use_cache=False)


def test_carto_auth_from_oauth(mocker, requests_mock):
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

    requests_mock.get(
        "https://accounts.app.carto.com/accounts",
        text="wrong json",
    )
    with pytest.raises(CredentialsError):
        CartoAuth.from_oauth(open_browser=False, use_cache=False)

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
        CartoAuth.from_oauth(open_browser=False, use_cache=False)

    requests_mock.get(
        "https://clausa.app.carto.com/config.yaml",
        text="""
        apis:
            baseUrl: "https://gcp-us-east1.api.carto.com"
        """,
    )
    carto_auth = CartoAuth.from_oauth(open_browser=False, use_cache=False)
    assert str(carto_auth.cache_filepath).endswith(".carto-auth/token.json")

    access_token = carto_auth.get_access_token()
    assert access_token == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX"

    cache_filepath = "fixtures/.carto_token_ok.json"
    fullpath = os.path.join(os.path.dirname(__file__), cache_filepath)
    carto_auth = CartoAuth.from_oauth(
        cache_filepath=fullpath, open_browser=False, use_cache=True
    )
    assert str(carto_auth.cache_filepath).endswith("fixtures/.carto_token_ok.json")


def test_handle_file_token_cached_on_file():
    cache_filepath = "fixtures/.carto_token_ok.json"
    fullpath = os.path.join(os.path.dirname(__file__), cache_filepath)
    carto_auth = CartoAuth(cache_filepath=fullpath)
    assert str(carto_auth.cache_filepath).endswith(cache_filepath)

    saved_token = "testAccessTokenlkjsdofiuqwelrkjas908d7"  # encoded on the file
    assert saved_token == carto_auth.get_access_token()

    expected_expiration_ts = 32503676400  # encoded on the file
    assert carto_auth._expiration_ts == expected_expiration_ts
    assert carto_auth._token_expired() is False


def test_handle_file_token_cached_expired_on_file():
    cache_filepath = "fixtures/.carto_token_expired.json"
    fullpath = os.path.join(os.path.dirname(__file__), cache_filepath)
    with pytest.raises(CredentialsError):
        CartoAuth(cache_filepath=fullpath)


def test_carto_dw_credentials(requests_mock):
    requests_mock.get(
        "https://gcp-us-east1.api.carto.com/v3/connections/carto-dw/token",
        json={
            "projectId": "project-id-mock",
            "token": "token-mock",
        },
    )
    cache_filepath = "fixtures/.carto_token_ok.json"
    fullpath = os.path.join(os.path.dirname(__file__), cache_filepath)
    carto_auth = CartoAuth(cache_filepath=fullpath)
    carto_dw_project_id, carto_dw_token = carto_auth.get_carto_dw_credentials()
    assert carto_dw_project_id == "project-id-mock"
    assert carto_dw_token == "token-mock"

    requests_mock.get(
        "https://gcp-us-east1.api.carto.com/v3/connections/carto-dw/token",
        text="wrong json",
    )
    cache_filepath = "fixtures/.carto_token_ok.json"
    fullpath = os.path.join(os.path.dirname(__file__), cache_filepath)
    with pytest.raises(CredentialsError):
        CartoAuth(cache_filepath=fullpath).get_carto_dw_credentials()

    requests_mock.get(
        "https://gcp-us-east1.api.carto.com/v3/connections/carto-dw/token",
        json={
            "token": "token-mock",
        },
    )
    cache_filepath = "fixtures/.carto_token_ok.json"
    fullpath = os.path.join(os.path.dirname(__file__), cache_filepath)
    with pytest.raises(CredentialsError):
        CartoAuth(cache_filepath=fullpath).get_carto_dw_credentials()


def test_carto_dw_client(requests_mock):
    from google.cloud.bigquery import Client

    requests_mock.get(
        "https://gcp-us-east1.api.carto.com/v3/connections/carto-dw/token",
        json={
            "projectId": "project-id-mock",
            "token": "token-mock",
        },
    )
    cache_filepath = "fixtures/.carto_token_ok.json"
    fullpath = os.path.join(os.path.dirname(__file__), cache_filepath)
    carto_auth = CartoAuth(cache_filepath=fullpath)

    bq_client = carto_auth.get_carto_dw_client()
    assert bq_client is not None

    assert hasattr(bq_client, "query")
    assert isinstance(bq_client, Client)


def test_get_access_token(requests_mock):
    access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InUzWjRJOVBhUVZ2RjA2MWVaZHlfNCJ9.eyJpc3MiOiJodHRwczovL29yYW1pcmV6LWF1dGguZXUuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTEwNjc5NzE5MDU5ODk3NjU5Njc4IiwiYXVkIjoiYXBpL2ZydWl0IiwiaWF0IjoxNjYxNzU4MTE1LCJleHAiOjE2NjE3NjUzMTUsImF6cCI6InN0TExYYnF1b2o2dnVOUDNCYUZaeEhmNE1UcFpLdWdhIiwic2NvcGUiOiJ3cml0ZTp1c3VhbC1mcnVpdCJ9.E5DbjwEOlbm37GkJPqkvh2ZZjlxtvERItd4loiWNcUXrzGQ34PBiC-kESeIFk_7AicldWxxGmIBZKycBflwoDNkR3CRchgW2CW4lPK7SSNAVR5iTwPPAHAhLwgwgKNmldOv5Wq7sDhf7Rc0JAQAdBqaTHXQrae57LNlnxVN--uJdq3oc4LYE3NDvQJIHlWaPDPsE6IgTOdQuS5bY867Ux3u3iLxEJpOevsce0d8l2or3se6GTX8rTb2Ip8rTkIrll0qzl-uwgTy0AoD-HM748W_FA1ScdTboilCzko6cFsMIDzb-ou-5BQPkIp6GtsYZuwrSD_t6t_ZrP46ehoUd1A"  # noqa: E501
    expire_in = 7200
    carto_auth = CartoAuth(access_token=access_token, expires_in=expire_in)
    ca_access_token = carto_auth.get_access_token()
    assert ca_access_token == access_token
    assert carto_auth._token_expired() is False

    requests_mock.post(
        "https://auth.carto.com/oauth/token",
        status_code=400,
    )

    carto_auth = CartoAuth(access_token=access_token, expires_in=-1, use_cache=False)
    with pytest.raises(CredentialsError):
        carto_auth.get_access_token()
