import importlib.util
from pathlib import Path

from workflow_py.base_objects.updater import Updater
from workflow_py.path_object.category.category_utils import get_host_categories
from workflow_py.path_object.dotfile.global_dotfile_utils import get_saved_global_dotfiles, is_global_dotfile_name
from workflow_py.path_object.dotfile.host_dotfile_utils import get_saved_host_dotfiles, is_host_dotfile_name
from workflow_py.var_store import make_trash_dir, VAR_STORE


class BasePuller(Updater):
    def pull_to_local(self):
        loaded_scripts = self.pull_scripts_to_local()
        loaded_global_files = self.pull_global_dotfiles_to_local()
        loaded_host_files = self.pull_host_dotfiles_to_local()
        loads = loaded_scripts + loaded_global_files + loaded_host_files
        if loads > 0:
            print(f"Loaded {loads} total files")

    # Scripts
    def pull_scripts_to_local(self):
        trash = self._get_trash_dir("local_scripts")
        num_writes = 0
        for category in get_host_categories():
            num_writes += category.write_to_local_script_dir(VAR_STORE.get_local_scripts_dir(), trash)
        if num_writes > 0:
            print(f"{num_writes} scripts loaded locally (old copies in {trash})")
        return num_writes

    # Dotfiles
    def pull_dotfiles_to_local(self):
        global_loads = self.pull_global_dotfiles_to_local()
        host_loads = self.pull_host_dotfiles_to_local()
        return global_loads + host_loads

    def pull_global_dotfiles_to_local(self) -> int:
        trash = self._get_trash_dir("local_global_dotfiles")
        num_writes = 0
        for saved_global_dotfile in get_saved_global_dotfiles():
            if is_global_dotfile_name(saved_global_dotfile.name):
                num_writes += saved_global_dotfile.write_to_dir(Path(VAR_STORE.home_dir), trash)
        if num_writes > 0:
            print(f"{num_writes} global dotfiles loaded locally (old copies in {trash})")
        return num_writes

    def pull_host_dotfiles_to_local(self) -> int:
        trash = self._get_trash_dir("local_host_dotfiles")
        num_writes = 0
        for saved_host_dotfile in get_saved_host_dotfiles():
            if is_host_dotfile_name(saved_host_dotfile.name):
                num_writes += saved_host_dotfile.write_to_dir(Path(VAR_STORE.home_dir), trash)
        if num_writes > 0:
            print(f"{num_writes} host dotfiles loaded locally (old copies in {trash})")
        return num_writes


def host_pull_to_local():
    path = VAR_STORE.get_host_dir() / "puller.py"
    print(f"Pulling to local for host {VAR_STORE.host}")
    assert path.is_file(), f"Puller script not found at {path}"
    module_name = path.stem
    module_spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    module.pull_to_local()


if __name__ == '__main__':
    host_pull_to_local()
