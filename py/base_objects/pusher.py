from pathlib import Path

from py.path_object.category.category_utils import get_host_categories
from py.path_object.dotfile.global_dotfile_utils import get_saved_global_dotfiles, is_global_dotfile_name
from py.path_object.dotfile.host_dotfile_utils import get_saved_host_dotfiles, is_host_dotfile_name
from py.var_store import VarStore, VAR_STORE, make_trash_dir


class BasePusher:
    var_store: VarStore
    trash_dir: Path

    def __init__(self):
        self.trash_dir = make_trash_dir(prefix="overwritten_saved_scripts")

    def push_to_saved(self):
        self.push_scripts_to_saved()
        self.push_dotfiles_to_saved()

    # Scripts
    def push_scripts_to_saved(self):
        overwrites = 0
        for category in get_host_categories():
            overwrites += category.read_from_local_script_dir(VAR_STORE.get_local_scripts_dir(), self.trash_dir)
        print(f"Overwrote {overwrites} scripts (old copies in {self.trash_dir})")

    # Dotfiles
    def _get_dotfile_trash(self) -> Path:
        dotfile_trash = Path(f"{self.trash_dir}/dotfiles")
        dotfile_trash.mkdir(exist_ok=True)
        return dotfile_trash

    def push_dotfiles_to_saved(self):
        self.push_global_dotfiles_to_saved()
        self.push_host_dotfiles_to_saved()

    def push_global_dotfiles_to_saved(self):
        dotfile_trash = self._get_dotfile_trash()
        for saved_global_dotfile in get_saved_global_dotfiles():
            if is_global_dotfile_name(saved_global_dotfile.name):
                saved_global_dotfile.read_from_dir(Path(VAR_STORE.home_dir), dotfile_trash)
        print(f"Pushed global dotfiles")

    def push_host_dotfiles_to_saved(self):
        dotfile_trash = self._get_dotfile_trash()
        for saved_host_dotfile in get_saved_host_dotfiles():
            if is_host_dotfile_name(saved_host_dotfile.name):
                saved_host_dotfile.read_from_dir(Path(VAR_STORE.home_dir), dotfile_trash)
        print(f"Pushed host specific dotfiles")


if __name__ == '__main__':
    BasePusher().push_to_saved()
