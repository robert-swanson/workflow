import shutil
from typing import Optional, List, Tuple
from pathlib import Path

from workflow_py.path_object.category.category import Category
from workflow_py.path_object.category.category_utils import get_host_categories
from workflow_py.path_object.script.script import Script
from workflow_py.var_store import VAR_STORE
from workflow_py.utils import fzf_select_one


def get_saved_script(name: str, category_name: Optional[str] = None) -> Tuple[Script, Category]:
    if category_name is not None:
        category = Category(VAR_STORE.get_scripts_dir() / category_name)
        assert category.path.is_dir(), f"Category {category_name} does not exist"
        script = Script(category.path / name)
        if not script.path.is_file():
            raise FileNotFoundError(f"{name} does not exist in category {category_name}")
        return script, category
    else:
        matched_script_categories: List[Tuple[Script, Category]] = []
        for category in get_host_categories():
            script = Script(category.path / name)
            if script.path.is_file():
                matched_script_categories.append((script, category))
        if len(matched_script_categories) == 0:
            raise FileNotFoundError(f"Script {name} does not exist in any category")
        elif len(matched_script_categories) > 1:
            raise FileNotFoundError(f"Script {name} exists in multiple categories (specify one): "
                                    f"{[category.name for script, category in matched_script_categories]}")
        else:
            return matched_script_categories[0]


def make_saved_script(name: str, category: Category, template: str) -> Script:
    validate_script_name_available(name)
    path = category.path / name

    template_path = VAR_STORE.get_script_templates_dir() / template
    assert template_path.is_file(), f"Template {template} does not exist at {template_path}"
    shutil.copyfile(template_path, path)
    script = Script(path)
    script.make_executable()
    return script


def validate_script_name_available(name: str):
    existing_categories = find_categories_with_script_name(name)
    assert len(existing_categories) == 0, f"Script {name} already exists in categories: {[category.name for category in existing_categories]}"
    available_in_local = not (VAR_STORE.get_local_scripts_dir() / name).is_file()
    assert available_in_local, f"Script {name} already exists in local scripts"


def find_categories_with_script_name(name: str) -> List[Category]:
    return [category for category in get_host_categories() if (category.path / name).is_file()]

def choose_template(prompt = None) -> Path:
    if not prompt:
        prompt = "Choose script template"
    templates = [f for f in (VAR_STORE.get_script_templates_dir()).iterdir()]
    return fzf_select_one(templates, prompt=prompt)
