import shutil
from pathlib import Path

from py.path_object.path_object import PathObject


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

    def write_to_dir(self, dest_dir: Path, trash_dir: Path):
        dest_script = Script(Path(f"{dest_dir}/{self.name}"))
        if dest_script.path.exists():
            shutil.move(dest_script.path, trash_dir)
        print(f"Writing {self.path} to {dest_script.path}")
        shutil.copy(self.path, dest_script.path)
        print(f"Overwrote {dest_script.path}")

    def read_from_dir(self, source_dir: Path, trash_dir: Path) -> bool:
        source_script = Script(Path(f"{source_dir}/{self.name}"))
        if not source_script.path.exists():
            print(f"Unable to update script, '{source_script.path}' does not exist")
            return False
        shutil.move(self.path, trash_dir)
        shutil.copy(source_script.path, self.path)
        print(f"Overwrote {self.path}")
        return True




