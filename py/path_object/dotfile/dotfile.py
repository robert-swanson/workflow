import shutil
from pathlib import Path

from py.path_object.path_object import PathObject


class Dotfile(PathObject):
    def write_to_dir(self, dest_dir: Path, trash_dir: Path):
        dest_path = Path(f"{dest_dir}/{self.name}")
        if dest_path.exists():
            shutil.move(dest_path, trash_dir)
        if self.path.is_file():
            shutil.copy(self.path, dest_path.parent)
        elif self.path.is_dir():
            shutil.copytree(self.path, dest_path)
        else:
            print(f"Unable to write dotfile, '{self.path}' is not a file or directory")
            raise ValueError

    def read_from_dir(self, source_dir: Path, trash_dir: Path) -> bool:
        source_path = Path(f"{source_dir}/{self.name}")
        if not source_path.exists():
            print(f"Unable to update dotfile, '{source_path}' does not exist")
            return False
        if self.path.exists():
            shutil.move(self.path, trash_dir)
        if source_path.is_file():
            shutil.copy(source_path, self.path.parent)
        elif source_path.is_dir():
            shutil.copytree(source_path, self.path)
        else:
            print(f"Unable to update dotfile, '{source_path}' is not a file or directory")
            raise ValueError
        return True
