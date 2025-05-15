import json
import os
from pathlib import Path

# Caminho padrão do arquivo de configuração
CONFIG_DIR = Path.home() / ".envscanner"
CONFIG_PATH = CONFIG_DIR / "config.json"

# Chaves permitidas no config
PROJECT_PATH_KEY = "project_path"
ROOT_PATH_KEY = "root_path"


def _ensure_config_file():
    """
    Garante que o diretório e o arquivo de configuração existam.
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        with open(CONFIG_PATH, "w") as f:
            json.dump({}, f)


def save_path(key: str, value: str):
    """
    Salva um caminho no arquivo de configuração.

    :param key: project_path ou root_path
    :param value: Caminho em string
    """
    _ensure_config_file()

    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)

    data[key] = value

    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)


def load_path(key: str) -> str | None:
    """
    Lê um caminho do arquivo de configuração.

    :param key: project_path ou root_path
    :return: Caminho salvo ou None
    """
    _ensure_config_file()

    with open(CONFIG_PATH, "r") as f:
        data = json.load(f)

    return data.get(key)