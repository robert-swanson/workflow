import shutil
import subprocess
from typing import Optional


def bash(*args):
    return subprocess.run(args)


def bash_txt(*args) -> str:
    return subprocess.run(args, capture_output=True, text=True).stdout.decode("utf-8")


def fzf_select(options: list[str], prompt: Optional[str] = None) -> str:
    if prompt is None:
        prompt = "Select one of the following"
    if shutil.which("fzf"):
        return bash_txt("fzf", *options)  # TODO: probably doesn't actually run fzf
    else:
        options = input(f"{prompt}: {options}:\n")
        assert options in options, f"Invalid selection: {options}"
        return options
