"""Helper functions for ipyfilechooser."""
import fnmatch
import os
import string
import sys
from typing import List, Sequence, Iterable, Optional


def get_subpaths(path: str) -> List[str]:
    """Walk a path and return a list of subpaths."""
    if os.path.isfile(path):
        path = os.path.dirname(path)

    paths = [path]
    path, tail = os.path.split(path)

    while tail:
        paths.append(path)
        path, tail = os.path.split(path)

    return paths


def strip_parent_path(path: str, parent_path: str) -> str:
    """Remove a parent path from a path."""
    if path.startswith(parent_path):
        return path[len(parent_path):]

    return path


def has_parent(path: str) -> bool:
    """Check if a path has a parent folder."""
    return os.path.basename(path) != ''


def has_parent_path(path: str, parent_path: str) -> bool:
    """Verifies if path falls under parent_path."""
    if parent_path:
        check = os.path.commonpath([path, parent_path]) == parent_path
    else:
        check = True

    return check


def match_item(item: str, filter_pattern: Sequence[str]) -> bool:
    """Check if a string matches one or more fnmatch patterns."""
    if isinstance(filter_pattern, str):
        filter_pattern = [filter_pattern]

    idx = 0
    found = False

    while idx < len(filter_pattern) and not found:
        found |= fnmatch.fnmatch(item.lower(), filter_pattern[idx].lower())
        idx += 1

    return found


def get_dir_contents(
        path: str,
        show_hidden: bool = False,
        prepend_icons: bool = False,
        show_only_dirs: bool = False,
        filter_pattern: Optional[Sequence[str]] = None,
        top_path: str = '') -> List[str]:
    """Get directory contents."""
    files = list()
    dirs = list()

    if os.path.isdir(path):
        for item in os.listdir(path):
            append = True
            if item.startswith('.') and not show_hidden:
                append = False
            full_item = os.path.join(path, item)
            if append and os.path.isdir(full_item):
                dirs.append(item)
            elif append and not show_only_dirs:
                if filter_pattern:
                    if match_item(item, filter_pattern):
                        files.append(item)
                else:
                    files.append(item)
        if has_parent(strip_parent_path(path, top_path)):
            dirs.insert(0, os.pardir)
    if prepend_icons:
        return prepend_dir_icons(sorted(dirs)) + sorted(files)
    else:
        return sorted(dirs) + sorted(files)


def prepend_dir_icons(dir_list: Iterable[str]) -> List[str]:
    """Prepend unicode folder icon to directory names."""
    return ['\U0001F4C1 ' + dirname for dirname in dir_list]


def get_drive_letters() -> List[str]:
    """Get all drive letters minus the drive used in path."""
    drives: List[str] = []

    if sys.platform == 'win32':
        # Windows has drive letters
        drives = [f'{d}:\\' for d in string.ascii_lowercase if os.path.exists(f'{d}:')]

    return drives


def is_valid_filename(filename: str) -> bool:
    """Verifies if a filename does not contain illegal character sequences"""
    valid = True
    valid = valid and os.pardir not in filename
    valid = valid and os.sep not in filename

    if os.altsep:
        valid = valid and os.altsep not in filename

    return valid


def normalize_path(path: str) -> str:
    """Normalize a path string."""
    normalized_path = ''

    if path:
        normalized_path = os.path.normpath(os.path.normcase(path))

    return normalized_path
