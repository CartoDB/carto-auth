import os
import sys
import json
import yaml
import datetime
import requests

from carto_auth.pkce import CartoPKCE
from carto_auth.errors import CredentialsError
from carto_auth.utils import get_cache_filepath, api_headers

DEFAULT_API_BASE_URL = "https://gcp-us-east1.api.carto.com"
OAUTH_TOKEN_URL = "https://auth.carto.com/oauth/token"


class CartoAuth:
    """CARTO Authentication object used to gather connect with the CARTO services.

    Args:
        api_base_url (str, optional): Base URL for a CARTO account.
        client_id (str, optional): Client id of a M2M application
            provided by CARTO.
        client_secret (str, optional): Client secret of a M2M application
            provided by CARTO.
        cache_filepath (str, optional): File path where the token is stored.
            Default "home()/.carto-auth/token.json".
        use_cache (bool, optional): Whether the stored cached token should be used.
            Default True.
        access_token (str, optional): Token already generated with CARTO.
        expires_in (str, optional): Time in seconds when the token will be expired.
    """

    def __init__(
        self,
        api_base_url=DEFAULT_API_BASE_URL,
        client_id=None,
        client_secret=None,
        cache_filepath=None,
        use_cache=True,
        access_token=None,
        expires_in=None,
    ):
        self.api_base_url = api_base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.cache_filepath = (
            get_cache_filepath() if cache_filepath is None else cache_filepath
        )
        self.use_cache = use_cache

        if access_token and expires_in:
            now = datetime.datetime.utcnow()
            expiration_ts = now + datetime.timedelta(seconds=expires_in)
            self._expiration_ts = expiration_ts.timestamp()
            self._access_token = access_token
            self._save_cached_token()
        else:
            if client_id and client_secret and api_base_url:
                self._expiration_ts = None
                self._access_token = None
            else:
                cached_token = self._load_cached_token()
                if not cached_token:
                    raise CredentialsError("Unable to locad cached token")

    @classmethod
    def from_oauth(
        cls,
        cache_filepath=None,
        use_cache=True,
        open_browser=True,
    ):
        """Create a CartoAuth object using OAuth with CARTO.

        Args:
            cache_filepath (str, optional): File path where the token is stored.
                Default "home()/.carto-auth/token.json".
            use_cache (bool, optional): Whether the stored cached token should be used.
                Default True.
            open_browser (bool, optional): Whether the web browser should be opened
                to authorize a user. Default True.
        """
        if cache_filepath is None:
            cache_filepath = get_cache_filepath()

        if cache_filepath and use_cache:
            try:
                return cls(cache_filepath=cache_filepath)
            except CredentialsError:
                pass

        carto_pkce = CartoPKCE(open_browser=open_browser)
        code = carto_pkce.get_auth_response()
        token_info = carto_pkce.get_token_info(code)
        api_base_url = get_api_base_url(token_info["access_token"])

        return cls(
            api_base_url=api_base_url,
            cache_filepath=cache_filepath,
            access_token=token_info["access_token"],
            expires_in=token_info["expires_in"],
        )

    @classmethod
    def from_file(cls, filepath, use_cache=True):
        """Create a CartoAuth object using CARTO credentials file.

        Args:
            filepath (str): File path of the CARTO credentials file.
            use_cache (bool, optional): Whether the stored cached token should be used.
                Default True.

        Raises:
            AttributeError: If the CARTO credentials file does not contain the
                attributes "api_base_url", "client_id", "client_secret".
            ValueError: If the CARTO credentials file does not contain any
                attribute value.
        """
        with open(filepath, "r") as f:
            content = json.load(f)
        for attr in ("api_base_url", "client_id", "client_secret"):
            if attr not in content:
                raise AttributeError(f"Missing attribute {attr} from {filepath}")
            if not content[attr]:
                raise ValueError(f"Missing value for {attr} in {filepath}")

        return cls(
            client_id=content["client_id"],
            client_secret=content["client_secret"],
            api_base_url=content["api_base_url"],
            use_cache=use_cache,
        )

    def get_carto_dw_credentials(self) -> tuple:
        """Get the CARTO Data Warehouse credentials.

        Returns:
            tuple: carto_dw_project, carto_dw_token.

        Raises:
            CredentialsError: If the API Base URL is not provided,
                the response is not JSON or has invalid attributes.
        """
        if not self.api_base_url:
            raise CredentialsError("api_base_url required")

        url = f"{self.api_base_url}/v3/connections/carto-dw/token"

        access_token = self.get_access_token()
        headers = api_headers(access_token)

        response = requests.get(url, headers=headers)

        try:
            creds = response.json()
        except requests.exceptions.JSONDecodeError:
            raise CredentialsError(
                "Invalid CARTO DW Token response. "
                "Please, make sure api_base_url is correctly defined"
            )

        if "projectId" in creds and "token" in creds:
            return creds["projectId"], creds["token"]

        raise CredentialsError(
            "Invalid attributes in CARTO DW Token response. "
            "Please, make sure api_base_url is correctly defined"
        )

    def get_carto_dw_client(self):
        """Returns a client to query directly the CARTO Data Warehouse.

        It requires extra dependencies carto-auth[carto-dw] to be installed.
        """
        try:
            from google.cloud.bigquery import Client
            from google.oauth2.credentials import Credentials
        except Exception:
            sys.stderr.write("Error: CARTO DW extension not found.\n")
            sys.stderr.write("Please, install carto-auth[carto-dw]\n")

        cdw_project, cdw_token = self.get_carto_dw_credentials()
        return Client(cdw_project, credentials=Credentials(cdw_token))

    def get_access_token(self):
        if self._access_token and not self._token_expired():
            return self._access_token

        stored_token = self._load_cached_token()
        if not stored_token or not self._access_token or self._token_expired():
            try:
                self._get_new_access_token()
            except CredentialsError:
                if stored_token and self._token_expired():
                    raise CredentialsError(
                        "Stored token expired but no client_id and client_secret found"
                    )
                else:
                    raise

        return self._access_token

    def _get_new_access_token(self):
        if not self.client_id or not self.client_secret:
            msg = "Missing "
            missing = []
            if not self.client_id:
                missing.append("client_id")
            if not self.client_secret:
                missing.append("client_secret")
            msg += " and ".join(missing)
            raise CredentialsError(msg)

        url = OAUTH_TOKEN_URL
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "audience": "carto-cloud-native-api",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code != 200:
            error_msg = response.json()
            error_subjects = {
                403: "Permissions Error",
                401: "Authorization Error",
            }
            error_subject = error_subjects.get(response.status_code, "Credential Error")
            msg = (
                f'{error_subject} - {error_msg.get("error")}: '
                f'{error_msg.get("error_description")}'
            )
            raise CredentialsError(msg)
        else:
            response_data = response.json()
            self._access_token = response_data["access_token"]
            self.token_type = response_data["token_type"]
            expires_in = response_data["expires_in"]
            now = datetime.datetime.utcnow()
            expiration_ts = now + datetime.timedelta(seconds=expires_in)
            self._expiration_ts = expiration_ts.timestamp()
            self._save_cached_token()

        return self._access_token

    def _token_expired(self):
        if not self._expiration_ts:
            return True

        now_utc_ts = datetime.datetime.utcnow().timestamp()

        return now_utc_ts > self._expiration_ts

    def _save_cached_token(self):
        if not self.use_cache or not self.cache_filepath:
            return False

        with open(self.cache_filepath, "w") as fw:
            info_to_cache = {
                "api_base_url": self.api_base_url,
                "access_token": self._access_token,
                "expiration_ts": self._expiration_ts,
            }
            json.dump(info_to_cache, fw)

        return True

    def _load_cached_token(self):
        if (
            not self.use_cache
            or not self.cache_filepath
            or not os.path.exists(self.cache_filepath)
        ):
            return False

        with open(self.cache_filepath, "r") as fr:
            info = json.load(fr)
            if (
                "api_base_url" in info
                and "access_token" in info
                and "expiration_ts" in info
            ):
                self.api_base_url = info["api_base_url"]
                self._access_token = info["access_token"]
                self._expiration_ts = info["expiration_ts"]
            else:
                return False

        if self._token_expired():
            return False

        return True


def get_api_base_url(access_token):
    url = "https://accounts.app.carto.com/accounts"
    headers = api_headers(access_token)

    response = requests.get(url, headers=headers)

    try:
        accounts = response.json()
    except requests.exceptions.JSONDecodeError:
        raise CredentialsError("Invalid Accounts response")

    tenant_domain = accounts.get("tenant_domain")

    if tenant_domain:
        url = f"https://{tenant_domain}/config.yaml"
        response = requests.get(url)

        try:
            config = yaml.safe_load(response.text)
            api_base_url = config.get("apis").get("baseUrl")
        except Exception:
            raise CredentialsError("Invalid Config response")

        return api_base_url
