import importlib.util
from pathlib import Path
from typing import Optional

from workflow_py.base_objects.updater import Updater
from workflow_py.path_object.category.category_utils import get_host_categories
from workflow_py.path_object.dotfile.global_dotfile_utils import get_saved_global_dotfiles, is_global_dotfile_name
from workflow_py.path_object.dotfile.host_dotfile_utils import get_saved_host_dotfiles, is_host_dotfile_name
from workflow_py.var_store import VarStore, VAR_STORE, make_trash_dir


class BasePusher(Updater):
    def push_to_saved(self):
        written_scripts = self.push_scripts_to_saved()
        written_global_files = self.push_global_dotfiles_to_saved()
        written_host_files = self.push_host_dotfiles_to_saved()
        writes = written_scripts + written_global_files + written_host_files
        if writes > 0:
            print(f"Saved {writes} total files")

    # Scripts
    def push_scripts_to_saved(self) -> int:
        num_writes = 0
        trash = self._get_trash_dir("saved_scripts")
        for category in get_host_categories():
            num_writes += category.read_from_local_script_dir(VAR_STORE.get_local_scripts_dir(), trash)
        if num_writes > 0:
            print(f"{num_writes} scripts saved (old saves in {trash})\n")
        return num_writes

    # Dotfiles
    def push_global_dotfiles_to_saved(self) -> int:
        num_writes = 0
        trash = self._get_trash_dir("saved_global_dotfiles")
        for saved_global_dotfile in get_saved_global_dotfiles():
            if is_global_dotfile_name(saved_global_dotfile.name):
                num_writes += saved_global_dotfile.read_from_dir(Path(VAR_STORE.home_dir), trash)
        if num_writes > 0:
            print(f"{num_writes} global dotfiles saved (old saves in {trash})\n")
        return num_writes

    def push_host_dotfiles_to_saved(self) -> int:
        num_writes = 0
        trash = self._get_trash_dir("saved_host_dotfiles")
        for saved_host_dotfile in get_saved_host_dotfiles():
            if is_host_dotfile_name(saved_host_dotfile.name):
                num_writes += saved_host_dotfile.read_from_dir(Path(VAR_STORE.home_dir), trash)
        if num_writes > 0:
            print(f"{num_writes} host dotfiles saved (old saves in {trash})\n")
        return num_writes


def host_push_to_saved():
    path = VAR_STORE.get_host_dir() / "pusher.py"
    print(f"Pushing to saved for host {VAR_STORE.host}")
    assert path.is_file(), f"Pusher script not found at {path}"
    module_name = path.stem
    module_spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    module.push_to_saved()


if __name__ == '__main__':
    host_push_to_saved()
