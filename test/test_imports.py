import importlib
from pathlib import Path


def walk_for_py(path):
    """
    Get all .py file in the specified directory.

    :Param path: the path of the target directory
    Returns an iterator of all the .py files under the target directory
    """
    for p in Path(path).iterdir():
        if p.is_dir():
            yield from walk_for_py(p)
        elif p.suffix == ".py":
            yield p


def test_import_all_files():
    python_files = walk_for_py("CatDataSchema")
    for python_file in python_files:
        if python_file.name == "__init__.py":
            # Make it its parent directory
            python_file = python_file.parent
        python_import_path = str(python_file).replace("/", ".")
        if python_import_path.endswith(".py"):
            python_import_path = python_import_path[:-3]
        if python_import_path.endswith(
            "alembic.env"
        ):  # env is only set up when running alembic command
            continue
        importlib.__import__(python_import_path)
