from py.path_object.dotfile.dotfile import Dotfile
from py.var_store import VAR_STORE


def get_saved_host_dotfiles() -> list[Dotfile]:
    return [Dotfile(dotfile) for dotfile in VAR_STORE.get_saved_host_dotfiles_dir().iterdir() if dotfile.is_file()]


def is_host_dotfile_name(name: str) -> bool:
    return name in [dotfile.name for dotfile in get_saved_host_dotfiles()]


def get_local_host_dotfiles() -> list[Dotfile]:
    return [Dotfile(dotfile) for dotfile in VAR_STORE.get_hidden_home_file_dirs() if is_host_dotfile_name(dotfile.name)]
