from workflow_py.path_object.script.script import Script
from workflow_py.var_store import VAR_STORE


def get_local_script(name: str) -> Script:
    script = Script(VAR_STORE.get_local_scripts_dir() / name)
    if not script.path.is_file():
        raise FileNotFoundError(f"{script.describe()} does not exist")
    return script

