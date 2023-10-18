import shutil
from pathlib import Path

from workflow_py.path_object.path_object import PathObject
from workflow_py.var_store import VAR_STORE


class Dotfile(PathObject):
    def __eq__(self, other):
        if other is self:
            return True
        if not self.name == other.name or type(other) != Dotfile:
            return False
        if self.path.exists() != other.path.exists():
            return False
        if self.path.is_file() != other.path.is_file():
            return False
        if self.path.is_dir():
            return all([Dotfile(self_file) == Dotfile(other_file) for self_file, other_file in zip(self.path.iterdir(), other.path.iterdir())])
        with open(self.path, 'r') as self_file, open(other.path, 'r') as other_file:
            return self_file.read() == other_file.read()

    def describe(self) -> str:
        global_dotfiles_dir = str(VAR_STORE.get_global_dotfiles_dir())
        host_dotfiles_dir = str(VAR_STORE.get_host_dir())
        if str(self.path).startswith(global_dotfiles_dir):
            return f"saved dotfile (global): {self.path.relative_to(global_dotfiles_dir)}"
        elif str(self.path).startswith(host_dotfiles_dir):
            return f"saved dotfile ({VAR_STORE.host}): {self.path.relative_to(host_dotfiles_dir)}"
        else:
            return f"local dotfile: {self.path.relative_to(VAR_STORE.home_dir)}"

    def __repr__(self):
        return self.describe()

    def write_to_dir(self, dest_dir: Path, trash_dir: Path):
        dest_dotfile = Dotfile(Path(f"{dest_dir}/{self.name}"))
        overwrite = self.path.exists()
        if not dest_dotfile.path.exists():
            print(f"Failed because the source does not exist")
            return False
        if self == dest_dotfile:
            return False

        print(f"\t{'Updating' if overwrite else 'Adding'} {dest_dotfile.describe()} <-- {self.describe()}")
        if overwrite:
            shutil.move(self.path, trash_dir)
        if dest_dotfile.path.is_file():
            shutil.copy(dest_dotfile.path, self.path.parent)
        elif dest_dotfile.path.is_dir():
            shutil.copytree(dest_dotfile.path, self.path)
        else:
            print(f"Failed because the source is not a file or directory")
            raise ValueError
        return overwrite

    def read_from_dir(self, source_dir: Path, trash_dir: Path) -> bool:
        source_dotfile = Dotfile(Path(f"{source_dir}/{self.name}"))
        return source_dotfile.write_to_dir(self.path.parent, trash_dir)
