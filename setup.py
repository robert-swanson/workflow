#!/usr/bin/python3
import os
import shutil
import socket
import sys

from workflow_py.base_objects.puller import host_pull_to_local
from workflow_py.path_object.category.category_utils import get_host_categories
from workflow_py.utils import fzf_select_multiple, confirm, fzf_select_one
from workflow_py.var_store import VAR_STORE

copy_hostname = VAR_STORE.host
VAR_STORE.host = socket.gethostname()
VAR_STORE.workflow_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
VAR_STORE.home_dir = os.path.expanduser("~")

category_names = [category.name for category in get_host_categories(get_all=True)]
pull_ignore_categories = fzf_select_multiple(category_names, "Select categories to ignore when pulling")
VAR_STORE.pull_ignore_categories.extend(pull_ignore_categories)

host_dir = VAR_STORE.get_host_dir()

if len([p.name for p in host_dir.iterdir()]) <= 1 or confirm("Host directory already exists. Overwrite?"):
    copy_host_dir = VAR_STORE.get_hosts_dir() / copy_hostname
    host_dir = VAR_STORE.get_host_dir()
    print(f"Copying {copy_host_dir} to {host_dir}")
    shutil.copytree(copy_host_dir, host_dir, dirs_exist_ok=True)
else:
    print(f"Skipping copy")

print("Saving VAR_STORE...")
VAR_STORE.write()

if confirm("Want to pull scripts into local?"):
    if len([d for d in VAR_STORE.get_local_scripts_dir().iterdir()]) > 0:
        if confirm("Local scripts directory is not empty, this may overwrite local copies. Continue?"):
            host_pull_to_local()
    host_pull_to_local()

if confirm("Add environment vars .bashrc?"):
    with open(os.path.expanduser("~/.bashrc"), "a") as file:
        file.write("\n\n# Workflow Setup\n")
        file.write(f'export WORKFLOW_PATH="{VAR_STORE.workflow_dir}"\n')
        file.write(f'export PATH="$PATH:$WORKFLOW_PATH/local_scripts"\n')
        file.write(f'export PYTHONPATH="$PYTHONPATH:$WORKFLOW_PATH"\n')
    print("Be sure to run `source ~/.bashrc` to apply changes")
print("Setup complete!")
