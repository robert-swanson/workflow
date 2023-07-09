#!/usr/bin/python3
import importlib
import os
import shutil
import socket
import sys
from pathlib import Path

from py.var_store import VarStore

print(f"Creating new workflow configuration for host {hostname} in {workflow_dir}")

category_names = [category.name for category in var_store.get_host_categories(get_all=True)]
pull_ignore_categories = input(f"Enter categories to ignore when pulling (comma separated): {category_names}\n")
for category_str in pull_ignore_categories.split(","):
    category_str = category_str.strip()
    assert category_str in category_names, f"Invalid category: {category_str}"
    var_store.pull_ignore_categories.append(category_str)

var_store.write()

host_dir = var_store.get_host_dir()
if not host_dir.exists():
    copy_hosts = [host.name for host in var_store.get_host_list()]
    copy_host = input(f"Which host would you like to copy from? {copy_hosts}: ")
    assert copy_host in copy_hosts, f"Invalid host: {copy_host}"
    copy_host_dir = Path(f"{var_store.get_hosts_dir()}/{copy_host}")
    print(f"Copying {copy_host_dir} to {host_dir}")
    shutil.copytree(copy_host_dir, host_dir)
    try:
        var_store.get_local_scripts_dir().mkdir(exist_ok=False)
    except FileExistsError:
        print(f"Directory {var_store.get_scripts_dir()} already exists. Running pull may overwrite local scripts")
else:
    print(f"Host directory {host_dir} already exists. Skipping copy.")

print("Running pull...")
var_store.run_pull_to_local()
