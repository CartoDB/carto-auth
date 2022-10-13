<!-- markdownlint-disable -->

<a href="../carto_auth/auth.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `auth`




**Global Variables**
---------------
- **DEFAULT_API_BASE_URL**
- **DEFAULT_CACHE_FILEPATH**


---

<a href="../carto_auth/auth.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CartoAuth`
CARTO Authentication object used to gather connect with the CARTO services.



**Args:**
  api_base_url (str, optional):
 - <b>`Base URL for a CARTO account. Default "https`</b>: //gcp-us-east1.api.carto.com". client_id (str, optional): Client id of a M2M application provided by CARTO. client_secret (str, optional): Client secret of a M2M application provided by CARTO. cache_filepath (str, optional): File path where the token is stored. Default ".carto_token.json". use_cache (bool, optional): Whether the stored cached token should be used. Default True. access_token (str, optional): Token already generated with CARTO. expires_in (str, optional): Time in seconds when the token will be expired.

How to get the API credentials:
 - <b>`https`</b>: //docs.carto.com/carto-user-manual/developers/carto-for-developers/

<a href="../carto_auth/auth.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    api_base_url='https://gcp-us-east1.api.carto.com',
    client_id=None,
    client_secret=None,
    cache_filepath='.carto_token.json',
    use_cache=True,
    access_token=None,
    expires_in=None
)
```








---

<a href="../carto_auth/auth.py#L110"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_file`

```python
from_file(filepath, use_cache=True)
```

Create a CartoAuth object using CARTO credentials file.



**Args:**
  filepath (str):  File path of the CARTO credentials file.  use_cache (bool, optional):  Whether the stored cached token should be used. Default True.



**Raises:**
  AttributeError  If the CARTO credentials file does not contain the following
 - <b>`attributes`</b>:  "client_id", "api_base_url", "client_secret". ValueError If the CARTO credentials file does not contain any attribute value.

---

<a href="../carto_auth/auth.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_oauth`

```python
from_oauth(
    api_base_url='https://gcp-us-east1.api.carto.com',
    cache_filepath='.carto_token.json',
    use_cache=True,
    open_browser=True
)
```

Create a CartoAuth object using OAuth with CARTO.



**Args:**

 - <b>`api_base_url`</b> (str, optional):  Base URL for a CARTO account.
 - <b>`Default "https`</b>: //gcp-us-east1.api.carto.com".
 - <b>`cache_filepath`</b> (str, optional):  File path where the token is stored.  Default ".carto_token.json".
 - <b>`use_cache`</b> (bool, optional):  Whether the stored cached token should be used.  Default True.
 - <b>`open_browser`</b> (bool, optional):  Whether the web browser should be opened  to authorize a user. Default True.

---

<a href="../carto_auth/auth.py#L177"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_access_token`

```python
get_access_token()
```





---

<a href="../carto_auth/auth.py#L162"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_carto_dw_client`

```python
get_carto_dw_client()
```

Returns a client to query directly the CARTO Data Warehouse.

It requires extra dependencies carto-auth[carto-dw] to be installed.

---

<a href="../carto_auth/auth.py#L142"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_carto_dw_credentials`

```python
get_carto_dw_credentials() → tuple
```

Get the CARTO Data Warehouse credentials.



**Returns:**

 - <b>`tuple`</b>:  carto_dw_project, carto_dw_token.



**Raises:**

 - <b>`CredentialsError`</b>:  If the API Base URL is not provided.
