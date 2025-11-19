# src/utils/url_parser.py
from urllib.parse import urlparse

def normalize_url(url: str) -> str:
    """
    Garante que a URL tenha esquema (http/https).
    Se o usuário digitar 'google.com', vira 'http://google.com'.
    """
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url

def parse_url(url: str) -> dict:
    """
    Retorna partes importantes da URL em um dicionário.
    """
    normalized = normalize_url(url)
    parsed = urlparse(normalized)

    host = parsed.hostname or ""
    path = parsed.path or "/"

    return {
        "original": url,
        "normalized": normalized,
        "scheme": parsed.scheme,
        "host": host,
        "path": path,
        "query": parsed.query,
    }
