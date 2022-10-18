from pathlib import Path


def get_home_dir():
    home_dir = Path.home() / ".carto-auth"
    home_dir.mkdir(parents=True, exist_ok=True)
    return home_dir


def get_cache_filepath():
    return get_home_dir() / "token.json"
