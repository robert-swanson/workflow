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
    assert selection in options, f"Invalid selection: {selection}"
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

    assert len(selections) >= min_required, f"Must select at least {min_required} selections"
    assert max_allowed is None or len(selections) <= max_allowed, f"Must select at most {max_allowed} selections"
    for selection in selections:
        assert selection in options, f"Invalid selection: {selection}"

    print(f"Selected {selections}")
    return selections


def confirm(prompt: str, fail_if_not=False) -> bool:
    response = input(f"{prompt} (y/N): ").lower() == "y"
    if fail_if_not and not response:
        exit(1)
    return response
