<!-- markdownlint-disable -->

<a href="../carto_auth/pkce.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `pkce`




**Global Variables**
---------------
- **OAUTH_AUTHORIZE_URL**
- **OAUTH_TOKEN_URL**
- **AUDIENCE**
- **CLIENT_ID**
- **REDIRECT_URI**
- **REDIRECT_URI_CLI**


---

<a href="../carto_auth/pkce.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CartoPKCE`
Implements PKCE Authorization Flow for client apps. 

<a href="../carto_auth/pkce.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(open_browser=True, org=None)
```

Creates PKCE Auth flow. 



**Args:**
 
 - <b>`open_browser`</b> (bool, optional):  Whether the web browser should be opened  to authorize a user. Default True, except when using Google Colab  or Databricks. 
 - <b>`org`</b> (str, optional):  Single Sign-On (SSO) organization in CARTO. 




---

<a href="../carto_auth/pkce.py#L97"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_auth_response`

```python
get_auth_response(open_browser=None)
```





---

<a href="../carto_auth/pkce.py#L156"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_authorization_code`

```python
get_authorization_code(response=None)
```





---

<a href="../carto_auth/pkce.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_authorize_url`

```python
get_authorize_url(state=None)
```





---

<a href="../carto_auth/pkce.py#L161"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_pkce_handshake_parameters`

```python
get_pkce_handshake_parameters()
```





---

<a href="../carto_auth/pkce.py#L165"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_token_info`

```python
get_token_info(code=None)
```





---

<a href="../carto_auth/pkce.py#L207"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `parse_response_code`

```python
parse_response_code(url)
```






---

<a href="../carto_auth/pkce.py#L223"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RequestHandler`







---

<a href="../carto_auth/pkce.py#L224"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `do_GET`

```python
do_GET()
```





---

<a href="../carto_auth/pkce.py#L251"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `log_message`

```python
log_message(format, *args)
```








