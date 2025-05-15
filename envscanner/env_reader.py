import os
from typing import Dict, Optional


def get_all_env_vars() -> Dict[str, str]:
    """
    Retorna todas as variáveis de ambiente visíveis ao Python.
    """
    return dict(os.environ)


def filter_env_vars(
    contains: Optional[str] = None,
    starts_with: Optional[str] = None,
    ends_with: Optional[str] = None
) -> Dict[str, str]:
    """
    Filtra variáveis de ambiente com base em critérios simples.

    :param contains: Substring que deve estar presente na chave
    :param starts_with: Prefixo obrigatório
    :param ends_with: Sufixo obrigatório
    :return: Dicionário de variáveis filtradas
    """
    all_vars = get_all_env_vars()
    result = {}

    for key, value in all_vars.items():
        if contains and contains not in key:
            continue
        if starts_with and not key.startswith(starts_with):
            continue
        if ends_with and not key.endswith(ends_with):
            continue
        result[key] = value

    return result
