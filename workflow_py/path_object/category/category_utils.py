from pathlib import Path

from workflow_py.path_object.category.category import Category
from workflow_py.utils import fzf_select_one
from workflow_py.var_store import VAR_STORE


def get_host_categories(get_all=False, category_regex="*") -> list[Category]:
    return [Category(category_dir) for category_dir in VAR_STORE.get_scripts_dir().rglob(category_regex)
            if category_dir.is_dir() and
            (get_all or category_dir.name not in VAR_STORE.pull_ignore_categories)]


def get_category_with_name(name: str) -> Category:
    category = Category(VAR_STORE.get_scripts_dir() / name)
    if not category.path.is_dir():
        possible_categories = get_host_categories(category_regex=f"*{name}*")
        if len(possible_categories) == 1:
            category = possible_categories[0]
        elif len(possible_categories) > 1:
            names = [cat.name for cat in possible_categories]
            name = fzf_select_one(names, prompt=f"'{name}' is not a category, did you mean:")
            category = Category(VAR_STORE.get_scripts_dir() / name)

    assert category.path.is_dir(), f"Category {name} does not exist"
    assert category.name not in VAR_STORE.pull_ignore_categories, f"Category {name} is ignored by this host"
    return category


def make_category_with_name(name: str) -> Category:
    print("cat: ", str(VAR_STORE.get_scripts_dir()) + "/" + str(name))
    category = Category(Path(str(VAR_STORE.get_scripts_dir()) + "/" + str(name)))
    assert not category.path.is_dir(), f"Category {name} already exists"
    assert category.name not in VAR_STORE.pull_ignore_categories, f"Category {name} exists but is ignored by this host"
    category.path.mkdir()
    return category

