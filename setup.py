#!/usr/bin/python3
import os
import shutil
import socket
import sys

from py.base_objects.puller import host_pull_to_local
from py.path_object.category.category_utils import get_host_categories
from py.utils import fzf_select_multiple, confirm
from py.var_store import VAR_STORE

copy_hostname = VAR_STORE.host
VAR_STORE.host = socket.gethostname()
VAR_STORE.workflow_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
VAR_STORE.home_dir = os.path.expanduser("~")

category_names = [category.name for category in get_host_categories(get_all=True)]
pull_ignore_categories = fzf_select_multiple(category_names, "Select categories to ignore when pulling")
VAR_STORE.pull_ignore_categories.extend(pull_ignore_categories)


host_dir = VAR_STORE.get_host_dir()
if not host_dir.exists():
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

if confirm("Want to save VAR_STORE?"):
    print("Saving VAR_STORE...")
    VAR_STORE.write()

if confirm("Want to pull?"):
    host_pull_to_local()

print(f"Check your bashrc to ensure that its pointing towards {VAR_STORE.workflow_dir}")
print("Setup complete!")

