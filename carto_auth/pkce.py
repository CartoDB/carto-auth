import os
import sys
import random
import logging
import secrets
import requests
import webbrowser

from urllib.parse import urlparse, urlencode
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qsl

from carto_auth.errors import CredentialsError

logger = logging.getLogger(__name__)


class CartoPKCE:
    """Implements PKCE Authorization Flow for client apps."""

    OAUTH_AUTHORIZE_URL = "https://auth.carto.com/authorize"
    OAUTH_TOKEN_URL = "https://auth.carto.com/oauth/token"
    AUDIENCE = "carto-cloud-native-api"
    CLIENT_ID = "AtxvHDeuXlR8XPfF2nj2Uv2I29pvmCxu"
    REDIRECT_URI = "http://localhost:10000/callback/"
    REDIRECT_URI_CLI = "https://callbacks.carto.com/token"

    def __init__(
        self,
        open_browser=True,
    ):
        """Creates PKCE Auth flow.

        Args:
            open_browser (bool, optional): Whether the web browser should be opened
                to authorize a user. Default True, except when using google.collab.
        """
        using_google_colab = "google.colab" in sys.modules
        using_databricks = "DATABRICKS_RUNTIME_VERSION" in os.environ
        self.open_browser = (
            False if (using_google_colab or using_databricks) else open_browser
        )

        self.redirect_uri = (
            self.REDIRECT_URI if self.open_browser else self.REDIRECT_URI_CLI
        )

        self._session = requests.Session()
        self._code_challenge_method = "S256"
        self._code_verifier = None
        self._code_challenge = None
        self._authorization_code = None

    @staticmethod
    def _get_code_verifier():
        length = random.randint(33, 96)
        return secrets.token_urlsafe(length)

    def _get_code_challenge(self):
        import base64
        import hashlib

        code_challenge_digest = hashlib.sha256(
            self._code_verifier.encode("utf-8")
        ).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge_digest).decode("utf-8")
        return code_challenge.replace("=", "")

    def _open_auth_url(self, state=None):
        auth_url = self.get_authorize_url(state)
        opened = webbrowser.open_new(auth_url)
        if opened:
            logger.info("Opened %s in your browser", auth_url)

    def get_authorize_url(self, state=None):
        if not self._code_challenge:
            self.get_pkce_handshake_parameters()
        payload = {
            "client_id": self.CLIENT_ID,
            "response_type": "code",
            "scope": None,
            "audience": self.AUDIENCE,
            "redirect_uri": self.redirect_uri,
            "code_challenge_method": self._code_challenge_method,
            "code_challenge": self._code_challenge,
        }
        if state is not None:
            payload["state"] = state
        urlparams = urlencode(payload)
        return "%s?%s" % (self.OAUTH_AUTHORIZE_URL, urlparams)

    def get_auth_response(self, open_browser=None):
        logger.info(
            "User authentication requires interaction with your "
            "web browser. Once you enter your credentials and "
            "give authorization, you will be redirected to "
            "a url.  Paste that url you were directed to to "
            "complete the authorization."
        )

        redirect_info = urlparse(self.redirect_uri)
        redirect_host, redirect_port = _get_host_port(redirect_info.netloc)

        if open_browser is None:
            open_browser = self.open_browser

        try:
            if (
                open_browser
                and redirect_host in ("127.0.0.1", "localhost")
                and redirect_info.scheme == "http"
            ):
                return self._get_auth_response_local_server(redirect_port)
        except Exception:
            self.redirect_uri = self.REDIRECT_URI_CLI
            return self._get_auth_response_interactive()

        return self._get_auth_response_interactive()

    def _get_auth_response_local_server(self, redirect_port):
        server = _start_local_http_server(redirect_port)
        self._open_auth_url()
        server.handle_request()

        if server.auth_code is not None:
            return server.auth_code
        elif server.error is not None:
            raise CredentialsError(
                "Received error from OAuth server: {}".format(server.error)
            )
        else:
            raise CredentialsError(
                "Server listening on localhost has not been accessed"
            )

    def _input(self, prompt):
        print(prompt)
        return input()

    def _get_auth_response_interactive(self):
        url = self.get_authorize_url()
        prompt = "Go to the following URL:\n{}\nEnter the Access code: ".format(url)
        response = self._input(prompt)
        if "code=" in response:
            state, code = self._parse_auth_response_url(response)
        else:
            # just in case the user just copy and paste the access code from the button
            code = response
        return code

    def get_authorization_code(self, response=None):
        if response:
            return self.parse_response_code(response)
        return self.get_auth_response()

    def get_pkce_handshake_parameters(self):
        self._code_verifier = self._get_code_verifier()
        self._code_challenge = self._get_code_challenge()

    def get_token_info(self, code=None):
        if self._code_verifier is None or self._code_challenge is None:
            self.get_pkce_handshake_parameters()

        payload = {
            "client_id": self.CLIENT_ID,
            "grant_type": "authorization_code",
            "audience": self.AUDIENCE,
            "code": code or self.get_authorization_code(),
            "redirect_uri": self.redirect_uri,
            "code_verifier": self._code_verifier,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        logger.debug(
            "sending POST request to %s with Headers: %s and Body: %r",
            self.OAUTH_TOKEN_URL,
            headers,
            payload,
        )

        try:
            response = self._session.post(
                self.OAUTH_TOKEN_URL,
                data=payload,
                headers=headers,
                verify=True,
            )
            response.raise_for_status()
            token_info = response.json()
            return token_info
        except requests.exceptions.HTTPError as http_error:
            raise CredentialsError.from_http_error(http_error)

    def parse_response_code(self, url):
        _, code = self._parse_auth_response_url(url)
        if code is None:
            return url
        else:
            return code

    @staticmethod
    def _parse_auth_response_url(url):
        query_s = urlparse(url).query
        form = dict(parse_qsl(query_s))
        if "error" in form:
            raise CredentialsError(f"Received error from auth server: {form['error']}")
        return tuple(form.get(param) for param in ["state", "code"])


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.server.auth_code = self.server.error = None
        try:
            state, auth_code = CartoPKCE._parse_auth_response_url(self.path)
            self.server.state = state
            self.server.auth_code = auth_code
        except Exception as error:
            self.server.error = error

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        if self.server.auth_code:
            callback_html = """<script>
            window.location.href = "https://callbacks.carto.com/success";
            </script>"""
        else:
            callback_html = """<script>
            window.location.href = "https://callbacks.carto.com/error";
            </script>"""

        self._write(callback_html)

    def _write(self, text):
        return self.wfile.write(text.encode("utf-8"))

    def log_message(self, format, *args):
        return


def _start_local_http_server(port, handler=RequestHandler):
    server = HTTPServer(("localhost", port), handler)
    server.allow_reuse_address = True
    server.auth_code = None
    server.auth_token_form = None
    server.error = None
    return server


def _get_host_port(netloc):
    if ":" in netloc:
        host, port = netloc.split(":", 1)
        port = int(port)
    else:
        host = netloc
        port = None

    return host, port
