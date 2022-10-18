from carto_auth.utils import get_cache_filepath


def test_get_cache_filepath():
    filepath = get_cache_filepath()
    assert str(filepath).endswith(".carto-auth/token.json")
