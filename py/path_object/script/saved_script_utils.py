from typing import Optional, List, Tuple

from py.path_object.category.category import Category
from py.path_object.category.category_utils import get_host_categories
from py.path_object.script.script import Script
from py.var_store import VAR_STORE


def get_saved_script(name: str, category_name: Optional[str] = None) -> Tuple[Script, Category]:
    if category_name is not None:
        category = Category(VAR_STORE.get_scripts_dir() / category_name)
        assert category.path.is_dir(), f"Category {category_name} does not exist"
        path = category.path / name
        if not path.is_file():
            raise FileNotFoundError(f"Script {name} does not exist in category {category_name}")
        return Script(path), category
    else:
        matched_script_categories: List[Tuple[Script, Category]] = []
        for category in get_host_categories():
            path = category.path / name
            if path.is_file():
                matched_script_categories.append((Script(path), category))
        if len(matched_script_categories) == 0:
            raise FileNotFoundError(f"Script {name} does not exist in any category")
        elif len(matched_script_categories) > 1:
            raise FileNotFoundError(f"Script {name} exists in multiple categories (specify one): "
                                    f"{[category.name for script, category in matched_script_categories]}")
        else:
            return matched_script_categories[0]
