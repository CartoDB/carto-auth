import sys
import json
import requests

from carto_auth.errors import CredentialsError
from carto_auth.utils import (
    get_cache_filepath,
    load_cache_file,
    save_cache_file,
    api_headers,
    is_token_expired,
    get_oauth_token_info,
    get_m2m_token_info,
    get_api_base_url,
)


class CartoAuth:
    """CARTO Authentication object used to gather connect with the CARTO services.

    Args:
        mode (str): Type of authentication: oauth, m2m.
        api_base_url (str, optional): Base URL for a CARTO account.
        access_token (str, optional): Token already generated with CARTO.
        expiration (int, optional): Time in seconds when the token will be expired.
        client_id (str, optional): Client id of a M2M application
            provided by CARTO.
        client_secret (str, optional): Client secret of a M2M application
            provided by CARTO.
        cache_filepath (str, optional): File path where the token is stored.
            Default "home()/.carto-auth/token.json".
        use_cache (bool, optional): Whether the stored cached token should be used.
            Default True.
        open_browser (bool, optional): Whether the web browser should be opened
            to authorize a user. Default True.
        org (str, optional): Single Sign-On (SSO) organization in CARTO.
    """

    def __init__(
        self,
        mode,
        api_base_url=None,
        access_token=None,
        expiration=None,
        client_id=None,
        client_secret=None,
        cache_filepath=None,
        use_cache=True,
        open_browser=True,
        org=None,
    ):
        self._mode = mode
        self._api_base_url = api_base_url
        self._cache_filepath = cache_filepath
        self._use_cache = use_cache
        self._org = org

        if mode == "oauth":
            self._access_token = access_token
            self._expiration = expiration
            self._open_browser = open_browser
        elif mode == "m2m":
            self._access_token = access_token
            self._expiration = expiration
            self._client_id = client_id
            self._client_secret = client_secret
        else:
            raise CredentialsError("Mode not supported. Available modes: oauth, m2m")

        self._save_cache_file()

    @classmethod
    def from_oauth(
        cls,
        cache_filepath=None,
        use_cache=True,
        open_browser=True,
        api_base_url=None,
        org=None,
    ):
        """Create a CartoAuth object using OAuth with CARTO.

        Args:
            cache_filepath (str, optional): File path where the token is stored.
                Default "home()/.carto-auth/token_oauth.json".
            use_cache (bool, optional): Whether the stored cached token should be used.
                Default True.
            open_browser (bool, optional): Whether the web browser should be opened
                to authorize a user. Default True.
            api_base_url (str, optional): Base URL for a CARTO account.
            org (str, optional): Single Sign-On (SSO) organization in CARTO.
        """
        mode = "oauth"

        if cache_filepath is None:
            cache_filepath = get_cache_filepath(mode)

        if use_cache:
            data = load_cache_file(cache_filepath)
            if (
                data
                and data.get("api_base_url")
                and not is_token_expired(data.get("expiration"))
            ):
                return cls(
                    mode=mode,
                    api_base_url=data.get("api_base_url"),
                    access_token=data.get("access_token"),
                    expiration=data.get("expiration"),
                    cache_filepath=cache_filepath,
                    use_cache=use_cache,
                    open_browser=open_browser,
                    org=org,
                )

        data = get_oauth_token_info(open_browser, org)
        return cls(
            mode=mode,
            api_base_url=api_base_url or get_api_base_url(data.get("access_token")),
            access_token=data.get("access_token"),
            expiration=data.get("expiration"),
            cache_filepath=cache_filepath,
            use_cache=use_cache,
            open_browser=open_browser,
            org=org,
        )

    @classmethod
    def from_m2m(cls, filepath, cache_filepath=None, use_cache=True):
        """Create a CartoAuth object using CARTO credentials file.

        Args:
            filepath (str): File path of the CARTO credentials file.
            cache_filepath (str, optional): File path where the token is stored.
                Default "home()/.carto-auth/token_m2m.json".
            use_cache (bool, optional): Whether the stored cached token should be used.
                Default True.

        Raises:
            AttributeError: If the CARTO credentials file does not contain the
                attributes "api_base_url", "client_id", "client_secret".
            ValueError: If the CARTO credentials file does not contain any
                attribute value.
        """
        mode = "m2m"

        with open(filepath, "r") as f:
            content = json.load(f)
        for attr in ("api_base_url", "client_id", "client_secret"):
            if attr not in content:
                raise AttributeError(f"Missing attribute {attr} from {filepath}")
            if not content[attr]:
                raise ValueError(f"Missing value for {attr} in {filepath}")

        api_base_url = content.get("api_base_url")
        client_id = content.get("client_id")
        client_secret = content.get("client_secret")

        if cache_filepath is None:
            cache_filepath = get_cache_filepath(mode)

        if use_cache:
            data = load_cache_file(cache_filepath)
            if (
                data
                and data.get("api_base_url")
                and not is_token_expired(data.get("expiration"))
            ):
                return cls(
                    mode=mode,
                    api_base_url=data.get("api_base_url"),
                    access_token=data.get("access_token"),
                    expiration=data.get("expiration"),
                    client_id=client_id,
                    client_secret=client_secret,
                    cache_filepath=cache_filepath,
                    use_cache=use_cache,
                )

        data = get_m2m_token_info(client_id, client_secret)
        return cls(
            mode=mode,
            api_base_url=api_base_url,
            access_token=data.get("access_token"),
            expiration=data.get("expiration"),
            client_id=client_id,
            client_secret=client_secret,
            cache_filepath=cache_filepath,
            use_cache=use_cache,
        )

    def get_api_base_url(self):
        return self._api_base_url

    def get_access_token(self):
        if self._access_token and not is_token_expired(self._expiration):
            return self._access_token

        # Token expired
        if self._mode == "oauth":
            data = get_oauth_token_info(self._open_browser, self._org)
        elif self._mode == "m2m":
            data = get_m2m_token_info(self._client_id, self._client_secret)

        self._access_token = data.get("access_token")
        self._expiration = data.get("expiration")
        self._save_cache_file()

        return self._access_token

    def get_carto_dw_credentials(self) -> tuple:
        """Get the CARTO Data Warehouse credentials.

        Returns:
            tuple: carto_dw_project, carto_dw_token.

        Raises:
            CredentialsError: If the API Base URL is not provided,
                the response is not JSON or has invalid attributes.
        """
        if not self._api_base_url:
            raise CredentialsError("api_base_url required")

        url = f"{self._api_base_url}/v3/connections/carto-dw/token"

        access_token = self.get_access_token()
        headers = api_headers(access_token)
        response = requests.get(url, headers=headers)

        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            raise CredentialsError(
                "Invalid CARTO DW Token response. "
                "Please, make sure api_base_url is correctly defined"
            )

        if "projectId" in response_data and "token" in response_data:
            return response_data["projectId"], response_data["token"]

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

    def _save_cache_file(self):
        if self._use_cache and self._cache_filepath:
            data = {
                "api_base_url": self._api_base_url,
                "access_token": self._access_token,
                "expiration": self._expiration,
            }
            save_cache_file(self._cache_filepath, data)
