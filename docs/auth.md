<!-- markdownlint-disable -->

<a href="../carto_auth/auth.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `auth`






---

<a href="../carto_auth/auth.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CartoAuth`
CARTO Authentication object used to gather connect with the CARTO services. 



**Args:**
 
 - <b>`mode`</b> (str):  Type of authentication: oauth, m2m. 
 - <b>`api_base_url`</b> (str, optional):  Base URL for a CARTO account. 
 - <b>`access_token`</b> (str, optional):  Token already generated with CARTO. 
 - <b>`expiration`</b> (int, optional):  Time in seconds when the token will be expired. 
 - <b>`client_id`</b> (str, optional):  Client id of a M2M application  provided by CARTO. 
 - <b>`client_secret`</b> (str, optional):  Client secret of a M2M application  provided by CARTO. 
 - <b>`cache_filepath`</b> (str, optional):  File path where the token is stored.  Default "home()/.carto-auth/token.json". 
 - <b>`use_cache`</b> (bool, optional):  Whether the stored cached token should be used.  Default True. 
 - <b>`open_browser`</b> (bool, optional):  Whether the web browser should be opened  to authorize a user. Default True. 

<a href="../carto_auth/auth.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    mode,
    api_base_url=None,
    access_token=None,
    expiration=None,
    client_id=None,
    client_secret=None,
    cache_filepath=None,
    use_cache=True,
    open_browser=True
)
```








---

<a href="../carto_auth/auth.py#L119"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_m2m`

```python
from_m2m(filepath, cache_filepath=None, use_cache=True)
```

Create a CartoAuth object using CARTO credentials file. 



**Args:**
 
 - <b>`filepath`</b> (str):  File path of the CARTO credentials file. 
 - <b>`cache_filepath`</b> (str, optional):  File path where the token is stored.  Default "home()/.carto-auth/token_m2m.json". 
 - <b>`use_cache`</b> (bool, optional):  Whether the stored cached token should be used.  Default True. 



**Raises:**
 
 - <b>`AttributeError`</b>:  If the CARTO credentials file does not contain the  attributes "api_base_url", "client_id", "client_secret". 
 - <b>`ValueError`</b>:  If the CARTO credentials file does not contain any  attribute value. 

---

<a href="../carto_auth/auth.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_oauth`

```python
from_oauth(cache_filepath=None, use_cache=True, open_browser=True)
```

Create a CartoAuth object using OAuth with CARTO. 



**Args:**
 
 - <b>`cache_filepath`</b> (str, optional):  File path where the token is stored.  Default "home()/.carto-auth/token_oauth.json". 
 - <b>`use_cache`</b> (bool, optional):  Whether the stored cached token should be used.  Default True. 
 - <b>`open_browser`</b> (bool, optional):  Whether the web browser should be opened  to authorize a user. Default True. 

---

<a href="../carto_auth/auth.py#L183"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_access_token`

```python
get_access_token()
```





---

<a href="../carto_auth/auth.py#L234"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_carto_dw_client`

```python
get_carto_dw_client()
```

Returns a client to query directly the CARTO Data Warehouse. 

It requires extra dependencies carto-auth[carto-dw] to be installed. 

---

<a href="../carto_auth/auth.py#L199"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_carto_dw_credentials`

```python
get_carto_dw_credentials() → tuple
```

Get the CARTO Data Warehouse credentials. 



**Returns:**
 
 - <b>`tuple`</b>:  carto_dw_project, carto_dw_token. 



**Raises:**
 
 - <b>`CredentialsError`</b>:  If the API Base URL is not provided,  the response is not JSON or has invalid attributes. 




