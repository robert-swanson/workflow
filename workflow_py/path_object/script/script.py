import os
import shutil
from pathlib import Path
from typing import Optional

from workflow_py.path_object.path_object import PathObject
from workflow_py.var_store import VAR_STORE


class Script(PathObject):
    def __eq__(self, other):
        if other is self:
            return True
        if not self.name == other.name or type(other) != Script:
            return False
        if self.path.exists() != other.path.exists():
            return False
        with open(self.path, 'r') as self_file, open(other.path, 'r') as other_file:
            return self_file.read() == other_file.read()

    def get_category(self) -> str:
        return self.path.parent.name

    def describe(self) -> str:
        local_scripts = str(VAR_STORE.get_local_scripts_dir())
        if str(self.path).startswith(local_scripts):
            return f"local script '{self.path.relative_to(local_scripts)}'"
        else:
            return f"saved script '{self.path.relative_to(VAR_STORE.get_scripts_dir())}'"

    def write_to_dir(self, dest_dir: Path, trash_dir: Optional[Path] = None) -> bool:
        dest_script = Script(Path(f"{dest_dir}/{self.name}"))
        if not self.path.exists():
            print(f"Cannot copy from {self.path} it does not exist")
            return False
        if self == dest_script:
            return False

        print(f"{'Updating' if dest_script.path.exists() else 'Adding'} {dest_script.describe()} <-- {self.describe()}")
        if dest_script.path.exists():
            assert trash_dir is not None, f"{dest_script.describe()} exists already (specify trash_dir if you want to overwrite it)"
            trash_dir.mkdir(exist_ok=True, parents=True)
            shutil.move(dest_script.path, trash_dir)
        shutil.copy(self.path, dest_script.path)
        Script(dest_script.path).make_executable()
        return True

    def read_from_dir(self, source_dir: Path, trash_dir: Path) -> bool:
        source_script = Script(Path(f"{source_dir}/{self.name}"))
        return source_script.write_to_dir(self.path.parent, trash_dir)

    def make_executable(self):
        os.chmod(self.path, 0o755)

    def delete(self, trash_dir: Path):
        try:
            shutil.move(self.path, trash_dir)
        except shutil.Error:
            self.path.unlink()
