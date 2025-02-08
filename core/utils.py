# ====================================================================================================
# @ Utilities
# ----------------------------------------------------------------------------------------------------
# 		General utility functions.
# ====================================================================================================
import inspect
import os
import sys
from importlib import import_module
from typing import List, Optional, Type


# ----------------------------------------------------------------------------------------------------
# * Import Classes
# ----------------------------------------------------------------------------------------------------
def import_classes(folder_name: str, class_type: Optional[Type] = None) -> List[Type]:
    """
    Import and return all classes defined inside modules in the given folder and its subfolders.

    Args:
        folder_name (str): Path to the folder, relative to the working directory.
        class_type (Optional[type]): If provided, only subclasses of this type are returned.

    Returns:
        List[type]: List of imported class types.
    """
    classes = []

    # Resolve the absolute path and add the parent directory to sys.path
    base_path = os.path.join(os.getcwd(), folder_name)
    parent_dir = os.path.dirname(base_path)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    if not os.path.exists(base_path) or not os.path.isdir(base_path):
        raise ValueError(
            f"Invalid folder: '{folder_name}' does not exist or is not a directory."
        )

    for root, _, files in os.walk(base_path):
        for file_name in files:
            if file_name.endswith(".py") and not file_name.startswith("__"):
                # Build module import path
                module_path = os.path.join(root, file_name)
                relative_module = os.path.relpath(module_path, parent_dir)
                module_name = relative_module.replace(os.sep, ".").removesuffix(".py")

                try:
                    module = import_module(module_name)
                except ModuleNotFoundError as e:
                    raise ModuleNotFoundError(
                        f"Import error: No module named '{module_name}'", e
                    )

                # Extract classes from the module
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # Ensure the class is defined in the current module
                    if obj.__module__ == module_name:
                        if class_type is None or issubclass(obj, class_type):
                            classes.append(obj)

    return classes


# ----------------------------------------------------------------------------------------------------
# * Draw UTF-8 Progress Bar
# ----------------------------------------------------------------------------------------------------
def draw_utf8_progress_bar(
    current: float,
    max: float,
    length: int = 5,
    filled_char: str = "█",
    empty_char: str = "░",
) -> str:
    if max == 0:
        max = current if current != 0 else 1
    normalized_value = int((current / max) * length)
    type(normalized_value)
    return (normalized_value * filled_char) + ((length - normalized_value) * empty_char)


# ----------------------------------------------------------------------------------------------------
# * Clamp
# ----------------------------------------------------------------------------------------------------
def clamp(
    value: int | float, min_value: int | float, max_value: int | float
) -> int | float:
    return max(min_value, min(value, max_value))
