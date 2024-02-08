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
should_overwrite = not host_dir.exists() or [p.name for p in host_dir.iterdir()] == ["var_store_bkup.json"]
print([p.name for p in host_dir.iterdir()])

if should_overwrite:
    copy_host_dir = VAR_STORE.get_hosts_dir() / copy_hostname
    host_dir = VAR_STORE.get_host_dir()
    print(f"Copying {copy_host_dir} to {host_dir}")
    shutil.copytree(copy_host_dir, host_dir)
    try:
        VAR_STORE.get_local_scripts_dir().mkdir(exist_ok=False)
    except FileExistsError:
        print(f"Directory {VAR_STORE.get_scripts_dir()} already exists. Running pull may overwrite local scripts")
else:
    print(f"Host directory {host_dir} already exists. Skipping copy.")

print("Saving VAR_STORE...")
VAR_STORE.write()

if confirm("Want to pull scripts into local?"):
    host_pull_to_local()

print(f"Check your bashrc to ensure that its pointing towards {VAR_STORE.workflow_dir}")
if confirm("Add environment vars .bashrc?"):
    with open(os.path.expanduser("~/.bashrc"), "a") as file:
        file.write("\n\n# Workflow Setup\n")
        file.write(f'export WORKFLOW_PATH="{VAR_STORE.workflow_dir}"\n')
        file.write(f'export PATH="$PATH:$WORKFLOW_PATH/workflow_scripts:$WORKFLOW_PATH/local_scripts"\n')
        file.write(f'export PYTHONPATH="$PYTHONPATH:$WORKFLOW_PATH"\n')
    print("Be sure to run `source ~/.bashrc` to apply changes")
print("Setup complete!")

