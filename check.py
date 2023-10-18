#!/usr/bin/env python3

import os
import sys
from pathlib import Path

sys.path.append(os.environ.get("WORKFLOW_PATH") or "~/workflow")

from workflow_py.utils import bash
from workflow_py.var_store import VAR_STORE

proj = Path(VAR_STORE.workflow_dir)

exclude_dir_paths: list[Path] = [VAR_STORE.get_local_scripts_dir(), proj/"venv"]
exclude_dirs: list[str] = [str(path.relative_to(proj)) for path in exclude_dir_paths]

exclude_args = []
for exclude_dir in exclude_dirs:
    exclude_args.append("--exclude")
    exclude_args.append(exclude_dir)

bash("mypy", str(proj), "--show-column-numbers", *exclude_args)
