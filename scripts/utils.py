from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_data_path() -> str:
    root_path = get_project_root().__str__()
    return f"{root_path}\\data"
