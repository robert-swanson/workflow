import json
import os
import socket
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

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
│   │   ├── script1
│   │   └── ...
│   └── ...
├── workflow_scripts
│   └── ...
└── setup.py
"""


@dataclass
class VarStore:
    host: str
    workflow_dir: str
    home_dir: str
    pull_ignore_categories: list[str]

    def write(self):
        with open(_get_var_store_path(), "w") as f:
            f.write(json.dumps(self.__dict__, indent=4))

    # Global Dotfiles
    def get_global_dotfiles_dir(self) -> Path:
        return Path(f"{self.workflow_dir}/dotfiles")

    # Hosts
    def get_hosts_dir(self) -> Path:
        return Path(f"{self.workflow_dir}/hosts/")

    def get_host_dir(self) -> Path:
        return Path(f"{self.get_hosts_dir()}/{self.host}")

    # Host Dotfiles
    def get_saved_host_dotfiles_dir(self) -> Path:
        return Path(f"{self.get_host_dir()}/dotfiles")

    # Local Scripts
    def get_local_scripts_dir(self) -> Path:
        return Path(f"{self.workflow_dir}/local_scripts")

    # Scripts / Categories
    def get_scripts_dir(self) -> Path:
        return Path(f"{self.workflow_dir}/scripts")

    # Workflow Scripts
    def get_workflow_scripts_dir(self) -> Path:
        return Path(f"{self.workflow_dir}/workflow_scripts")


# Trash
def make_trash_dir(prefix: str) -> Path:
    trash_dir = Path(f"/tmp/workflow_trash_{prefix}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
    trash_dir.mkdir(exist_ok=False)
    return trash_dir


def _get_var_store_path() -> Path:
    script_path = Path(__file__).resolve()
    return Path(script_path.parent.parent / "var_store.json")


def _load_var_store() -> VarStore:
    if "VAR_STORE" in globals():
        return globals()["VAR_STORE"]
    path = _get_var_store_path()
    if path.is_file():
        return json.loads(open(path, "r").read(), object_hook=lambda d: VarStore(**d))
    else:
        hostname = socket.gethostname()
        workflow_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        home_directory = os.path.expanduser("~")
        print(f"Warning, using empty var store with hostname {hostname}")
        return VarStore(hostname, workflow_dir, home_directory, [])


VAR_STORE = _load_var_store()
