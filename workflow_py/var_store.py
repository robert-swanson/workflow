import json
import os
import socket
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from workflow_py.utils import fzf_select_one

"""
workflow
├── dotfiles
│   └── ...
├── hosts
│   ├── host1
│   │   ├── dotfiles
│   │   │   └── ...
│   │   ├── pull
│   │   └── push
│   └── ...
├── local_scripts (gitignored)
│   └── ...
├── scripts
│   ├── category1 (optionally gitignored)
│   │   ├── category1.1
│   │   │   └── script 1.1
│   │   ├── script1
│   │   └── ...
│   ├── workflow_scripts 
│   │   └── ...
│   └── ...
└── setup.py
"""


@dataclass
class VarStore:
    host: str
    workflow_dir: str
    home_dir: str
    pull_ignore_categories: list[str]
    export_ignore_categories: list[str]

    def write(self):
        with open(_get_var_store_path(), "w") as f:
            f.write(json.dumps(self.__dict__, indent=4))
        with open(_get_var_store_bkup_path(self.host), "w") as f:
            f.write(json.dumps(self.__dict__, indent=4))

    # Global Dotfiles
    def get_global_dotfiles_dir(self) -> Path:
        return make_assured_dir(f"{self.workflow_dir}/dotfiles")

    # Hosts
    def get_hosts_dir(self) -> Path:
        return make_assured_dir(f"{self.workflow_dir}/hosts/")

    def get_host_dir(self) -> Path:
        return make_assured_dir(f"{self.get_hosts_dir()}/{self.host}")

    def get_saved_host_dotfiles_dir(self) -> Path:
        return make_assured_dir(f"{self.get_host_dir()}/dotfiles")

    def get_script_templates_dir(self) -> Path:
        return make_assured_dir(f"{self.get_host_dir()}/script_templates")

    # Local Scripts
    def get_local_scripts_dir(self) -> Path:
        return make_assured_dir(f"{self.workflow_dir}/local_scripts")

    # Scripts / Categories
    def get_scripts_dir(self) -> Path:
        return make_assured_dir(f"{self.workflow_dir}/scripts")

    # Workflow Scripts
    def get_workflow_scripts_dir(self) -> Path:
        return make_assured_dir(f"{self.workflow_dir}/scripts/workflow_scripts")


def make_assured_dir(path_str: str) -> Path:
    path = Path(path_str)
    path.mkdir(exist_ok=True, parents=True)
    return path


# Trash
def make_trash_dir(name: Optional[str] = None) -> Path:
    trash_dir = Path(f"/tmp/workflow_trash/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}{f'_{name}' if name else ''}")
    trash_dir.mkdir(exist_ok=True, parents=True)
    return trash_dir


def _get_var_store_bkup_path(host: str) -> Path:
    script_path = Path(__file__).resolve()
    return Path(script_path.parent.parent / f"hosts/{host}/var_store_bkup.json")


def _get_var_store_path() -> Path:
    script_path = Path(__file__).resolve()
    return Path(script_path.parent.parent / "var_store.json")


def _deserialize_var_store(path: Path) -> VarStore:
    return json.loads(open(path, "r").read(), object_hook=lambda d: VarStore(**d))


def _load_var_store() -> VarStore:
    if "VAR_STORE" in globals():
        return globals()["VAR_STORE"]
    path = _get_var_store_path()
    if path.is_file():
        return _deserialize_var_store(path)
    else:
        hostname = socket.gethostname()
        workflow_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

        print(f"No var store found for {hostname}, specify one of the following to copy from:")
        hosts = [str(path.name) for path in Path(f"{workflow_dir}/hosts").iterdir() if path.is_dir()]
        copy_host = fzf_select_one(hosts)

        return _deserialize_var_store(_get_var_store_bkup_path(copy_host))


def get_hidden_home_file_dirs() -> list[Path]:
    return [path for path in Path(VAR_STORE.home_dir).iterdir() if path.name.startswith(".")]


VAR_STORE = _load_var_store()
