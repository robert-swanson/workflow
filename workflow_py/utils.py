import shutil
import subprocess
from typing import Optional


def bash(*args, print_cmd=False):
    if print_cmd:
        print(" ".join(args))
    return subprocess.run(args)


def bash_txt(*args) -> str:
    return subprocess.run(args, capture_output=True, text=True).stdout


def fzf_select_one(options: list[str], prompt: Optional[str] = None) -> str:
    if shutil.which("fzf"):
        path = "/tmp/fzf_input"
        with open(path, "w") as file:
            file.write("\n".join(options))
        options_pipe = subprocess.Popen(["cat", path], stdout=subprocess.PIPE)
        fzf_args = (["--prompt", prompt] if prompt is not None else [])
        fzf = subprocess.Popen(["fzf"] + fzf_args, stdin=options_pipe.stdout, stdout=subprocess.PIPE)
        selection = fzf.communicate()[0].decode("utf-8").strip()
    else:
        if prompt is None:
            prompt = "Select one of the following"
        selection = input(f"{prompt}: {options}:\n")

    if selection not in options:
        print(f"Invalid selection: {selection}")
        return fzf_select_one(options, prompt)

    print(f"Selected {selection}")
    return selection


def fzf_select_multiple(options: list[str], prompt: Optional[str] = None, min_required=0, max_allowed=None) \
        -> list[str]:
    if shutil.which("fzf"):
        path = "/tmp/fzf_input"
        with open(path, "w") as file:
            file.write("\n".join(options))
        options_pipe = subprocess.Popen(["cat", path], stdout=subprocess.PIPE)
        fzf_args = (["--prompt", prompt] if prompt is not None else []) + ['--multi'] + (
            [max_allowed] if max_allowed is not None else [])
        fzf = subprocess.Popen(["fzf"] + fzf_args, stdin=options_pipe.stdout, stdout=subprocess.PIPE)
        output = fzf.communicate()[0].decode("utf-8").strip()
        selections = output.split("\n")
    else:
        if prompt is None:
            prompt = "Select zero or more of the following, separated by commas"
        selections = input(f"{prompt}: {options}:\n").split(",")

    selections = [selection.strip() for selection in selections]
    is_valid = True

    if len(selections) < min_required:
        print(f"Must select at least {min_required} selections")
        is_valid = False

    if max_allowed is not None and len(selections) > max_allowed:
        print(f"Must select at most {max_allowed} selections")
        is_valid = False

    for selection in selections:
        if selection not in options:
            print(f"Invalid selection: {selection}")
            is_valid = False

    if not is_valid:
        return fzf_select_multiple(options, prompt, min_required, max_allowed)

    print(f"Selected {selections}")
    return selections


def confirm(prompt: str, fail_if_not=False) -> bool:
    response = input(f"{prompt} (y/N): ").lower() == "y"
    if fail_if_not and not response:
        exit(1)
    return response
