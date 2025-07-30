"""(module) path."""

import os


def is_valid(path: str, file_type: str = "jpg"):
    """Checks if file on the {path} exists, is a file and is of type {file_type}.

    Args:
        path (str): Path of the file to check.
        file_type (str): File type of file. Needs to work with doctr.io.DocumentFile and PIL.Image. By default "jpg".

    Returns:
        Boolean: True if all conditions are met, otherwise False.
    """
    if not os.path.exists(path):
        return False
    if not os.path.isfile(path):
        return False
    if not path.endswith(file_type):
        return False

    return True


def is_valid_dir(path: str):
    """Checks if directory on the {path} exists, is a directory.

    Args:
        path (str): Path of the file to check.

    Returns:
        Boolean: True if all conditions are met, otherwise False.
    """
    if not os.path.exists(path):
        return False
    if not os.path.isfile(path):
        return False

    return True
