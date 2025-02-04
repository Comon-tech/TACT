import tomllib

with open("pyproject.toml", "rb") as file:
    PYPROJECT = tomllib.load(file)
    PROJECT = PYPROJECT["project"]
    TASKS = PYPROJECT["tool"]["taskipy"]["tasks"]
