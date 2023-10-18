from workflow_py.path_object.category.category import Category
from workflow_py.var_store import VAR_STORE


def get_host_categories(get_all=False) -> list[Category]:
    return [Category(category_dir) for category_dir in VAR_STORE.get_scripts_dir().iterdir()
            if category_dir.is_dir() and
            (get_all or category_dir.name not in VAR_STORE.pull_ignore_categories)]


def get_category_with_name(name: str) -> Category:
    category = Category(VAR_STORE.get_scripts_dir() / name)
    assert category.path.is_dir(), f"Category {name} does not exist"
    assert category.name not in VAR_STORE.pull_ignore_categories, f"Category {name} is ignored by this host"
    return category


def make_category_with_name(name: str) -> Category:
    category = Category(VAR_STORE.get_scripts_dir() / name)
    assert not category.path.is_dir(), f"Category {name} already exists"
    assert category.name not in VAR_STORE.pull_ignore_categories, f"Category {name} exists but is ignored by this host"
    category.path.mkdir()
    return category

