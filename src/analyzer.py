# src/analyzer.py
from typing import Dict, List

from utils.url_parser import parse_url
from utils.indicators import build_indicators
from blacklist_checker import is_in_blacklist

def analyze_url(url: str) -> Dict:
    """
    Analisa a URL e retorna um dicionário com:
      - status (safe/malicious/suspicious)
      - motivos (lista de strings)
      - indicadores (booleans)
    """
    parsed = parse_url(url)
    indicators = build_indicators(parsed)

    reasons: List[str] = []

    # 1) Verificação em "lista" de phishing
    in_blacklist, reason_blacklist = is_in_blacklist(parsed["host"])
    if in_blacklist:
        reasons.append(reason_blacklist)

    # 2) Heurísticas simples
    if indicators["number_letter_substitution"]:
        reasons.append("Presença de números em substituição a letras no domínio.")
    if indicators["many_subdomains"]:
        reasons.append("Uso excessivo de subdomínios (muitos pontos no domínio).")
    if indicators["special_chars"]:
        reasons.append("Presença de caracteres especiais suspeitos na URL (@, %, =, &).")

    # Define status com base nos motivos encontrados
    if in_blacklist:
        status = "malicious"
    elif reasons:
        status = "suspicious"
    else:
        status = "safe"

    return {
        "input_url": url,
        "parsed": parsed,
        "status": status,
        "reasons": reasons,
        "indicators": indicators,
    }
