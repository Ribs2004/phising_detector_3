# src/utils/indicators.py
import re

def has_number_letter_substitution(host: str) -> bool:
    """
    Verifica se existem padrões suspeitos de substituição de letras por números,
    ex: g00gle, paypa1, micr0soft.
    Isso não é perfeito, mas serve como heurística simples.
    """
    suspicious_pairs = [
        ("0", "o"),
        ("1", "l"),
        ("3", "e"),
        ("5", "s"),
        ("7", "t"),
    ]
    host_lower = host.lower()
    for num, _ in suspicious_pairs:
        if num in host_lower:
            return True
    return False

def has_many_subdomains(host: str, max_ok: int = 3) -> bool:
    """
    Verifica se há muitos subdomínios.
    Ex: login.secure.update.account.example.com (muitos pontos).
    """
    # Divide pelo ponto e conta quantas partes há.
    parts = host.split(".")
    return len(parts) > max_ok

def has_special_chars_in_url(url: str) -> bool:
    """
    Verifica presença de caracteres especiais suspeitos na URL.
    Não é exato, mas ajuda: @, %, =, & etc.
    """
    suspicious_chars = ["@", "%", "=", "&"]
    return any(ch in url for ch in suspicious_chars)

def build_indicators(parsed_url: dict) -> dict:
    """
    Retorna um dicionário com indicadores simples para a URL.
    """
    host = parsed_url.get("host", "")
    normalized = parsed_url.get("normalized", "")

    indicators = {
        "number_letter_substitution": has_number_letter_substitution(host),
        "many_subdomains": has_many_subdomains(host),
        "special_chars": has_special_chars_in_url(normalized),
    }

    return indicators
