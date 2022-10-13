<!-- markdownlint-disable -->

<a href="../carto_auth/pkce.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `pkce`






---

<a href="../carto_auth/pkce.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CartoPKCE`
Implements PKCE Authorization Flow for client apps.

<a href="../carto_auth/pkce.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(open_browser=True)
```

Creates PKCE Auth flow.



**Args:**

 - <b>`open_browser`</b> (bool, optional):  Whether the web browser should be opened  to authorize a user. Default True, except when using google.collab.




---

<a href="../carto_auth/pkce.py#L92"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_auth_response`

```python
get_auth_response(open_browser=None)
```





---

<a href="../carto_auth/pkce.py#L151"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_authorization_code`

```python
get_authorization_code(response=None)
```





---

<a href="../carto_auth/pkce.py#L75"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_authorize_url`

```python
get_authorize_url(state=None)
```





---

<a href="../carto_auth/pkce.py#L156"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_pkce_handshake_parameters`

```python
get_pkce_handshake_parameters()
```





---

<a href="../carto_auth/pkce.py#L160"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_token_info`

```python
get_token_info(code=None)
```





---

<a href="../carto_auth/pkce.py#L195"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `parse_response_code`

```python
parse_response_code(url)
```






---

<a href="../carto_auth/pkce.py#L211"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RequestHandler`







---

<a href="../carto_auth/pkce.py#L212"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `do_GET`

```python
do_GET()
```





---

<a href="../carto_auth/pkce.py#L239"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `log_message`

```python
log_message(format, *args)
```
