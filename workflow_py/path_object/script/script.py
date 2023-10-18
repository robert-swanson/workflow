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

    def write_to_dir(self, dest_dir: Path, trash_dir: Optional[Path] = None):
        dest_script = Script(Path(f"{dest_dir}/{self.name}"))
        if dest_script.path.exists():
            assert trash_dir is not None, f"Script {self.name} already exists in {dest_dir} (specify trash_dir if you want to overwrite it)"
            shutil.move(dest_script.path, trash_dir)
            print(f"Overwrote {dest_script.path}")
        print(f"Writing {self.path} to {dest_script.path}")
        shutil.copy(self.path, dest_script.path)
        Script(dest_script.path).make_executable()

    def read_from_dir(self, source_dir: Path, trash_dir: Path) -> bool:
        source_script = Script(Path(f"{source_dir}/{self.name}"))
        if not source_script.path.exists():
            print(f"Unable to update script, '{source_script.path}' does not exist")
            return False
        shutil.move(self.path, trash_dir)
        shutil.copy(source_script.path, self.path)
        self.make_executable()
        print(f"Overwrote {self.path}")
        return True

    def make_executable(self):
        os.chmod(self.path, 0o755)

    def delete(self, trash_dir: Path):
        try:
            shutil.move(self.path, trash_dir)
        except shutil.Error:
            self.path.unlink()
