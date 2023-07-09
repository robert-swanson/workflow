from pathlib import Path

from py.path_object.category.category_utils import get_host_categories
from py.path_object.dotfile.global_dotfile_utils import get_saved_global_dotfiles, is_global_dotfile_name
from py.path_object.dotfile.host_dotfile_utils import get_saved_host_dotfiles, is_host_dotfile_name
from py.var_store import VarStore, make_trash_dir


class BasePuller:
    var_store: VarStore
    trash_dir: Path

    def __init__(self):
        self.trash_dir = make_trash_dir(prefix="overwritten_local_scripts")

    def pull_to_local(self):
        self.pull_scripts_to_local()
        self.pull_host_dotfiles_to_local()
        self.pull_global_dotfiles_to_local()

    # Scripts
    def pull_scripts_to_local(self):
        overwrites = 0
        for category in get_host_categories():
            overwrites += category.write_to_local_script_dir(self.var_store.get_local_scripts_dir(), self.trash_dir)
        print(f"Overwrote {overwrites} scripts (old copies in {self.trash_dir})")

    # Dotfiles
    def _get_dotfile_trash(self) -> Path:
        dotfile_trash = Path(f"{self.trash_dir}/dotfiles")
        dotfile_trash.mkdir(exist_ok=True)
        return dotfile_trash

    def pull_dotfiles_to_local(self):
        self.pull_global_dotfiles_to_local()
        self.pull_host_dotfiles_to_local()

    def pull_global_dotfiles_to_local(self):
        dotfile_trash = self._get_dotfile_trash()
        for saved_global_dotfile in get_saved_global_dotfiles():
            if is_global_dotfile_name(saved_global_dotfile.name):
                saved_global_dotfile.write_to_dir(Path(self.var_store.home_dir), dotfile_trash)
        print(f"Pulled global dotfiles")

    def pull_host_dotfiles_to_local(self):
        dotfile_trash = self._get_dotfile_trash()
        for saved_host_dotfile in get_saved_host_dotfiles():
            if is_host_dotfile_name(saved_host_dotfile.name):
                saved_host_dotfile.write_to_dir(Path(self.var_store.home_dir), dotfile_trash)
        print(f"Pulled host specific dotfiles")


if __name__ == '__main__':
    BasePuller().pull_to_local()