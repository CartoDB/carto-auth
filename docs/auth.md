<!-- markdownlint-disable -->

<a href="../carto_auth/auth.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `auth`




**Global Variables**
---------------
- **DEFAULT_API_BASE_URL**


---

<a href="../carto_auth/auth.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CartoAuth`
CARTO Authentication object used to gather connect with the CARTO services. 



**Args:**
 
 - <b>`api_base_url`</b> (str, optional):  Base URL for a CARTO account. 
 - <b>`client_id`</b> (str, optional):  Client id of a M2M application  provided by CARTO. 
 - <b>`client_secret`</b> (str, optional):  Client secret of a M2M application  provided by CARTO. 
 - <b>`cache_filepath`</b> (str, optional):  File path where the token is stored.  Default "home()/.carto-auth/token.json". 
 - <b>`use_cache`</b> (bool, optional):  Whether the stored cached token should be used.  Default True. 
 - <b>`access_token`</b> (str, optional):  Token already generated with CARTO. 
 - <b>`expires_in`</b> (str, optional):  Time in seconds when the token will be expired. 

<a href="../carto_auth/auth.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    api_base_url='https://gcp-us-east1.api.carto.com',
    client_id=None,
    client_secret=None,
    cache_filepath=None,
    use_cache=True,
    access_token=None,
    expires_in=None
)
```








---

<a href="../carto_auth/auth.py#L108"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_file`

```python
from_file(filepath, use_cache=True)
```

Create a CartoAuth object using CARTO credentials file. 



**Args:**
 
 - <b>`filepath`</b> (str):  File path of the CARTO credentials file. 
 - <b>`use_cache`</b> (bool, optional):  Whether the stored cached token should be used.  Default True. 



**Raises:**
 
 - <b>`AttributeError`</b>:  If the CARTO credentials file does not contain the  attributes "client_id", "api_base_url", "client_secret". 
 - <b>`ValueError`</b>:  If the CARTO credentials file does not contain any  attribute value. 

---

<a href="../carto_auth/auth.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_oauth`

```python
from_oauth(
    api_base_url='https://gcp-us-east1.api.carto.com',
    cache_filepath=None,
    use_cache=True,
    open_browser=True
)
```

Create a CartoAuth object using OAuth with CARTO. 



**Args:**
 
 - <b>`api_base_url`</b> (str, optional):  Base URL for a CARTO account. 
 - <b>`cache_filepath`</b> (str, optional):  File path where the token is stored.  Default "home()/.carto-auth/token.json". 
 - <b>`use_cache`</b> (bool, optional):  Whether the stored cached token should be used.  Default True. 
 - <b>`open_browser`</b> (bool, optional):  Whether the web browser should be opened  to authorize a user. Default True. 

---

<a href="../carto_auth/auth.py#L173"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_access_token`

```python
get_access_token()
```





---

<a href="../carto_auth/auth.py#L158"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_carto_dw_client`

```python
get_carto_dw_client()
```

Returns a client to query directly the CARTO Data Warehouse. 

It requires extra dependencies carto-auth[carto-dw] to be installed. 

---

<a href="../carto_auth/auth.py#L138"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_carto_dw_credentials`

```python
get_carto_dw_credentials() → tuple
```

Get the CARTO Data Warehouse credentials. 



**Returns:**
 
 - <b>`tuple`</b>:  carto_dw_project, carto_dw_token. 



**Raises:**
 
 - <b>`CredentialsError`</b>:  If the API Base URL is not provided. 




