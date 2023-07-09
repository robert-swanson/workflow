from py.path_object.category.category import Category
from py.var_store import VAR_STORE


def get_host_categories(get_all=False) -> list[Category]:
    return [Category(category_dir) for category_dir in VAR_STORE.get_scripts_dir().iterdir()
            if category_dir.is_dir() and
            (get_all or category_dir.name not in VAR_STORE.pull_ignore_categories)]

