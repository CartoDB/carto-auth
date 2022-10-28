from urllib.parse import urlparse, parse_qs

from carto_auth.pkce import CartoPKCE


def test_url_properly_created():
    carto_pkce = CartoPKCE(open_browser=False)
    url = carto_pkce.get_authorize_url()
    parsed_url = urlparse(url)
    parsed_qs = parse_qs(parsed_url.query)

    assert parsed_qs["code_challenge_method"] == ["S256"]
    assert parsed_qs["redirect_uri"] == ["https://app.carto.com/auth/token"]
    assert parsed_qs["response_type"] == ["code"]
    assert parsed_qs["client_id"][0] == "0dxb8HR3ATXCxJiPOJVHsLoHoAtbRX6u"
    assert len(parsed_qs["code_challenge"]) > 0


def test_token_from_input_prompt(mocker, requests_mock):
    mocker.patch(
        "carto_auth.pkce.CartoPKCE._input",
        return_value="carto.com/autorize?code=abcde",
    )
    requests_mock.post(
        "https://auth.carto.com/oauth/token",
        json={
            "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpX",
            "scope": "read:tokens write:tokens read:imports write:imports "
            "read:connections write:connections",
            "expires_in": 86400,
            "token_type": "Bearer",
        },
    )

    carto_pkce = CartoPKCE(open_browser=False)
    carto_pkce.get_pkce_handshake_parameters()

    assert len(carto_pkce._code_challenge) > 0
    assert len(carto_pkce._code_verifier) > 0


def test_token_from_input_mocked(mocker, requests_mock):
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

    carto_pkce = CartoPKCE(open_browser=False)
    code = carto_pkce.get_auth_response()
    assert code == "abcde"

    mocker.patch(
        "webbrowser.open_new",
        return_value=True,
    )

    carto_pkce = CartoPKCE(open_browser=True)
    code = carto_pkce.get_auth_response()
    assert code == "abcde"
