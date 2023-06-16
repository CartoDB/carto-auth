import os
import json
import yaml
import requests

from pathlib import Path
from datetime import datetime, timedelta

from carto_auth.pkce import CartoPKCE
from carto_auth.errors import CredentialsError


def api_headers(access_token):
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }


def get_oauth_token_info(open_browser=True, org=None):
    carto_pkce = CartoPKCE(open_browser=open_browser, org=org)
    code = carto_pkce.get_auth_response()
    return carto_pkce.get_token_info(code)


def get_m2m_token_info(client_id, client_secret):
    url = "https://auth.carto.com/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "audience": "carto-cloud-native-api",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(url, headers=headers, data=data)

    try:
        response_data = response.json()
    except requests.exceptions.JSONDecodeError:
        raise CredentialsError(
            "Invalid M2M Token response. "
            "Please, make sure client_id and client_secret are correctly defined"
        )

    if "access_token" in response_data and "expires_in" in response_data:
        access_token = response_data["access_token"]
        expires_in = response_data["expires_in"]
        expiration = int(
            (datetime.utcnow() + timedelta(seconds=expires_in)).timestamp()
        )
        return {
            "access_token": access_token,
            "expiration": expiration,
        }

    raise CredentialsError(
        "Invalid attributes in M2M Token response. "
        "Please, make sure client_id and client_secret are correctly defined"
    )


def get_api_base_url(access_token):
    url = "https://accounts.app.carto.com/accounts"
    headers = api_headers(access_token)
    response = requests.get(url, headers=headers)

    try:
        response_data = response.json()
    except requests.exceptions.JSONDecodeError:
        raise CredentialsError("Invalid Accounts response")

    if response_data.get("error"):
        raise CredentialsError(response_data.get("error"))

    tenant_domain = response_data.get("tenant_domain")

    if tenant_domain:
        url = f"https://{tenant_domain}/config.yaml"
        response = requests.get(url)

        try:
            config = yaml.safe_load(response.text)
            api_base_url = config.get("apis").get("baseUrl")
        except Exception:
            raise CredentialsError("Invalid Config response")

        return api_base_url


def get_home_dir():
    home_dir = Path.home() / ".carto-auth"
    home_dir.mkdir(parents=True, exist_ok=True)
    return home_dir


def get_cache_filepath(mode):
    return get_home_dir() / f"token_{mode}.json"


def load_cache_file(cache_filepath):
    if cache_filepath and os.path.exists(cache_filepath):
        with open(cache_filepath, "r") as f:
            data = json.load(f)
            if (
                "api_base_url" in data
                and "access_token" in data
                and "expiration" in data
            ):
                return data


def save_cache_file(cache_filepath, data):
    with open(cache_filepath, "w") as f:
        if "api_base_url" in data and "access_token" in data and "expiration" in data:
            json.dump(data, f)


def is_token_expired(expiration):
    if not expiration:
        return True

    now = datetime.utcnow().timestamp()

    return now > expiration
