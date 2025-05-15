import typer
from pathlib import Path
from envscanner import config, project_path, env_reader  # novo import


app = typer.Typer(help="Tool thats scan and identifies Ambient Variables.")

# Command to define the path of the project
@app.command()
def set_path(path: str):
    """
    Sets the Absolute Path of the current project.
    """
    full_path = Path(path).resolve()
    project_path.save_path("project_path", str(full_path))
    typer.echo(f"Project Path seted: {full_path}")


# Command to define the root path of all projects (if in network)
@app.command()
def set_root(path: str):
    """
    Sets the root Path where your projects are located.
    It´s recomended if your projects is in a Network Path!
    """
    root_path = Path(path).resolve()
    project_path.save_path("root_path", str(root_path))
    typer.echo(f"Root Path seted: {root_path}")


# Command to run the Scanner (placeholder)
@app.command()
def scan():
    """
    Escaneia as variáveis de ambiente com base no settings.json.
    """
    try:
        settings = config.load_settings()
        typer.echo(f"Projeto: {settings['project_name']}")
        typer.echo(f"Ambiente: {settings['environment_variable']}")
    except config.ConfigError as e:
        typer.echo(f"Erro ao carregar settings: {e}")


@app.command()
def list_envs(
    contains: str = typer.Option(None, help="Filtra variáveis que contêm essa substring."),
    starts_with: str = typer.Option(None, help="Filtra variáveis que começam com esse prefixo."),
    ends_with: str = typer.Option(None, help="Filtra variáveis que terminam com esse sufixo."),
):
    """
    Lista variáveis de ambiente do sistema, com filtros opcionais.
    """
    variable = env_reader.filter_env_vars(
        contains=contains,
        starts_with=starts_with,
        ends_with=ends_with,
    )

    if not variable:
        typer.echo("Nenhuma variável encontrada com os critérios fornecidos.")
    else:
        for key, value in variable.items():
            typer.echo(f"{key} = {value}")
    

if __name__ == "__main__":
    app()