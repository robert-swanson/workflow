from py.path_object.script.script import Script
from py.var_store import VAR_STORE


def get_local_script(name: str) -> Script:
    path = VAR_STORE.get_local_scripts_dir() / name
    if not path.is_file():
        raise FileNotFoundError(f"Script {name} does not exist")
    return Script(path)

