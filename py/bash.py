import subprocess


def bash(*args):
    return subprocess.run(args)
