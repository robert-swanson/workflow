from pathlib import Path
from typing import Optional

from workflow_py.var_store import make_trash_dir


class Updater:
    _trash_dir: Path

    def __init__(self):
        self._trash_dir = make_trash_dir()

    def _get_trash_dir(self, name: Optional[str] = None):
        if name is None:
            dotfile_trash = Path(f"{self._trash_dir}")
        else:
            dotfile_trash = Path(f"{self._trash_dir}/{name}")
        dotfile_trash.mkdir(exist_ok=True)
        return dotfile_trash
