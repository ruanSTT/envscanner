import json
from pathlib import Path
from envscanner import project_path

SETTINGS_FILENAME = "settings.json"
DEFAULT_ENV = "Development"


class ConfigError(Exception):
    pass


def load_settings() -> dict:
    """
    Carrega o arquivo settings.json com base nos caminhos definidos.

    Retorna:
        dicionário com os dados do settings.json
    Lança:
        ConfigError se não conseguir localizar ou carregar o settings.json
    """
    # 1. Tenta carregar a partir do caminho do projeto
    project_dir = project_path.load_path("project_path")
    settings_path = None

    if project_dir:
        settings_path = Path(project_dir) / SETTINGS_FILENAME
        if not settings_path.exists():
            settings_path = None

    # 2. Se não encontrou, tenta usar root_path + project_name
    if not settings_path:
        root_dir = project_path.load_path("root_path")
        if not root_dir:
            raise ConfigError("Nenhum caminho definido (project_path ou root_path).")

        try:
            # Leitura temporária para extrair project_name
            fallback_settings = Path.cwd() / SETTINGS_FILENAME
            if not fallback_settings.exists():
                raise ConfigError("Arquivo settings.json não encontrado no diretório atual.")
            
            with open(fallback_settings, "r") as f:
                settings_data = json.load(f)
                project_name = settings_data["project_name"]

            project_dir = Path(root_dir) / project_name
            settings_path = project_dir / SETTINGS_FILENAME

            if not settings_path.exists():
                raise ConfigError(f"Arquivo settings.json não encontrado em: {settings_path}")

        except KeyError:
            raise ConfigError("O campo 'project_name' é obrigatório no settings.json.")

    # Carregar o settings.json final
    with open(settings_path, "r") as f:
        settings = json.load(f)

    # Garante campo environment_variable
    if "environment_variable" not in settings:
        settings["environment_variable"] = DEFAULT_ENV

    return settings