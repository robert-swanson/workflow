import os.path
from pathlib import Path

from workflow_py.path_object.path_object import PathObject
from workflow_py.path_object.script.script import Script
from workflow_py.var_store import VAR_STORE


class Category(PathObject):
    def __init__(self, path: Path):
        self.name = str(os.path.relpath(path, VAR_STORE.get_scripts_dir()))
        self.path = path

    def get_scripts(self) -> list[Script]:
        return [Script(script) for script in self.path.iterdir() if script.is_file()]

    def write_to_local_script_dir(self, dest_dir: Path, trash_dir: Path) -> int:
        category_trash = Path(f"{trash_dir}/{self.name}")
        num_overwrites = 0
        for script in self.get_scripts():
            new_script = Script(Path(f"{dest_dir}/{script.name}"))
            if new_script != script:
                num_overwrites += 1
                script.write_to_dir(dest_dir, category_trash)
        return num_overwrites

    def read_from_local_script_dir(self, local_script_dir: Path, trash_dir: Path) -> int:
        category_trash = Path(f"{trash_dir}/{self.name}")
        num_overwrites = 0
        for existing_saved_script in self.get_scripts():
            local_script = Script(Path(f"{local_script_dir}/{existing_saved_script.name}"))
            if local_script != existing_saved_script:
                num_overwrites += existing_saved_script.read_from_dir(local_script_dir, category_trash)
        return num_overwrites

    def get_saved_scripts(self) -> list[Script]:
        return [Script(path) for path in self.path.iterdir() if path.is_file()]
