from typing import Tuple, Set
from urllib.parse import urlparse
from functools import lru_cache
import os
import csv

from utils.url_parser import normalize_url

# Caminho para o arquivo CSV com URLs maliciosas
DATA_FILE = os.path.join(
    os.path.dirname(__file__), "..", "data", "malicious_phish.csv"
)


@lru_cache(maxsize=1)
def load_phishing_hosts() -> Set[str]:
    """
    Carrega hosts de URLs de phishing a partir do dataset local malicious_phish.csv.

    - Descobre dinamicamente as colunas de URL e de tipo.
    - Normaliza as URLs (garante http:// ou https://).
    - Ignora linhas que gerarem erro (ex: URLs muito quebradas, IPv6 malformado).
    """
    hosts: Set[str] = set()

    try:
        print(f"[INFO] Carregando dataset local de phishing em {DATA_FILE}...")
        with open(DATA_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            fieldnames = [name.lower() for name in (reader.fieldnames or [])]
            print(f"[INFO] Colunas encontradas no CSV: {fieldnames}")

            possible_url_cols = ["url", "urls", "link"]
            url_col = next((c for c in possible_url_cols if c in fieldnames), None)

            possible_type_cols = ["type", "label", "category", "class"]
            type_col = next((c for c in possible_type_cols if c in fieldnames), None)

            if not url_col:
                print("[WARN] Nenhuma coluna de URL encontrada (url/urls/link).")
                return hosts

            if not type_col:
                print("[WARN] Nenhuma coluna de tipo encontrada (type/label/category/class).")
                print("[WARN] Considerando todas as linhas como phishing PARA TESTE.")

            count_rows = 0
            count_phishing = 0
            count_skipped = 0

            for row in reader:
                count_rows += 1

                try:
                    row_lower = {k.lower(): v for k, v in row.items()}

                    url = (row_lower.get(url_col) or "").strip()
                    if not url:
                        continue

                    if type_col:
                        url_type = (row_lower.get(type_col) or "").strip().lower()
                        if url_type not in {"phish", "phishing"}:
                            continue
                    else:
                        url_type = "phishing"

                    normalized = normalize_url(url)
                    parsed = urlparse(normalized)
                    host = parsed.hostname

                    if not host:
                        continue

                    count_phishing += 1
                    hosts.add(host.lower())

                except Exception as e_row:
                    # Essa é a linha que estava te dando "Invalid IPv6 URL"
                    # Agora a gente só ignora essa linha e segue o loop.
                    count_skipped += 1
                    # Se quiser ver qual linha deu erro, descomenta a próxima linha:
                    # print(f"[DEBUG] Linha pulada ({count_rows}): {e_row}")
                    continue

            print(
                f"[INFO] Linhas lidas do CSV: {count_rows}. "
                f"URLs tratadas como phishing: {count_phishing}. "
                f"Hosts únicos carregados: {len(hosts)}. "
                f"Linhas puladas por erro: {count_skipped}."
            )

    except FileNotFoundError:
        print(f"[WARN] Arquivo malicious_phish.csv não encontrado em {DATA_FILE}.")
    except Exception as e:
        print(f"[WARN] Erro ao abrir dataset local: {e}")

    return hosts


def is_in_blacklist(host: str) -> Tuple[bool, str]:
    """
    Verifica se o host está no conjunto de hosts de phishing
    carregados a partir do dataset local.
    """
    if not host:
        return False, ""

    host = host.lower()
    hosts = load_phishing_hosts()

    print(f"[DEBUG] Verificando host '{host}' contra {len(hosts)} hosts do dataset local.")

    if host in hosts:
        return True, "Domínio encontrado no dataset local de URLs de phishing (malicious_phish.csv)."

    return False, ""
