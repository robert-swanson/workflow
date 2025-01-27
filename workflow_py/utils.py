import shutil
import subprocess
from typing import Optional, TypeVar


def bash(*args, print_cmd=False):
    if print_cmd:
        print(" ".join(args))
    return subprocess.run(args)


def bash_txt(*args) -> str:
    return subprocess.run(args, capture_output=True, text=True).stdout

T = TypeVar("T")

def fzf_select_one(options: list[T], prompt: Optional[str] = None) -> T:
    stringified_options: list[str] = [str(option) for option in options]
    if (len(set(stringified_options)) != len(stringified_options)):
        prompt += " (warning, list contains duplicates)"
    if shutil.which("fzf"):
        path = "/tmp/fzf_input"
        with open(path, "w") as file:
            file.write("\n".join(stringified_options))
        options_pipe = subprocess.Popen(["cat", path], stdout=subprocess.PIPE)
        fzf_args = (["--prompt", prompt] if prompt is not None else [])
        fzf = subprocess.Popen(["fzf"] + fzf_args, stdin=options_pipe.stdout, stdout=subprocess.PIPE)
        selection = fzf.communicate()[0].decode("utf-8").strip()
    else:
        if prompt is None:
            prompt = "Select one of the following"
        selection = input(f"{prompt}: {stringified_options}:\n")

    if not selection:
        print("Exiting due to no selection")
        exit()

    if selection not in stringified_options:
        print(f"Invalid selection: {selection}")
        input("Press enter to try again")
        return fzf_select_one(options, prompt)

    print(f"Selected {selection}")
    return options[stringified_options.index(selection)]


def fzf_select_multiple(options: list[T], prompt: Optional[str] = None, min_required=0, max_allowed=None, print_selection=True) \
        -> list[T]:
    stringified_options: list[str] = [str(option) for option in options]
    if (len(set(stringified_options)) != len(stringified_options)):
        prompt += " (warning, list contains duplicates)"

    if shutil.which("fzf"):
        path = "/tmp/fzf_input"
        with open(path, "w") as file:
            file.write("\n".join(stringified_options))
        options_pipe = subprocess.Popen(["cat", path], stdout=subprocess.PIPE)
        fzf_args = (["--prompt", prompt] if prompt is not None else []) + \
            (['--multi'] + [str(max_allowed)]) if max_allowed is not None else []
        fzf = subprocess.Popen(["fzf"] + fzf_args, stdin=options_pipe.stdout, stdout=subprocess.PIPE)
        output = fzf.communicate()[0].decode("utf-8").strip()
        stringified_selections = output.split("\n")
    else:
        if prompt is None:
            prompt = "Select zero or more of the following, separated by commas"
        stringified_selections = input(f"{prompt}: {stringified_options}:\n").split(",")

    stringified_selections = [selection.strip() for selection in stringified_selections]
    is_valid = True

    if min_required == 0 and stringified_selections == [""]:
        return []

    if len(stringified_selections) < min_required:
        print(f"Must select at least {min_required} selections")
        is_valid = False

    if max_allowed is not None and len(stringified_selections) > max_allowed:
        print(f"Must select at most {max_allowed} selections")
        is_valid = False

    selections = []
    for selection in stringified_selections:
        if selection not in stringified_options:
            print(f"Invalid selection: {selection}")
            is_valid = False
        selections.append(options[stringified_options.index(selection)])

    if not is_valid:
        input("Press enter to try again")
        return fzf_select_multiple(options, prompt, min_required, max_allowed)

    if print_selection:
        print(f"Selected {selections}")
    return selections


def confirm(prompt: str, fail_if_not=False) -> bool:
    response = input(f"{prompt} (y/N): ").lower() == "y"
    if fail_if_not and not response:
        exit(1)
    return response

