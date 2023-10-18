from pathlib import Path


class PathObject:
    name: str
    path: Path

    def __init__(self, path: Path):
        self.name = path.name
        self.path = path

    def describe(self) -> str:
        return str(self.path)

    def __repr__(self):
        return self.name
