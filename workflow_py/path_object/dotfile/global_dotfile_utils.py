from pathlib import Path

from workflow_py.path_object.dotfile.dotfile import Dotfile
from workflow_py.path_object.dotfile.host_dotfile_utils import is_host_dotfile_name
from workflow_py.var_store import VAR_STORE


def get_hidden_home_file_dirs() -> list[Path]:
    return [path for path in Path(VAR_STORE.home_dir).iterdir() if path.name.startswith(".")]


def is_global_dotfile_name(name: str) -> bool:
    return name in [dotfile.name for dotfile in get_saved_global_dotfiles()]


def get_saved_global_dotfiles() -> list[Dotfile]:
    return [Dotfile(path) for path in VAR_STORE.get_global_dotfiles_dir().iterdir()
            if not is_host_dotfile_name(path.name)]


def get_local_global_dotfiles() -> list[Dotfile]:
    return [Dotfile(path) for path in get_hidden_home_file_dirs()
            if path.name in get_saved_global_dotfiles()]
