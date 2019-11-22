import os


def get_subpaths(path):
    """Walk a path and return a list of subpaths"""
    if os.path.isfile(path):
        path = os.path.dirname(path)

    paths = [path]
    path, tail = os.path.split(path)

    while tail:
        paths.append(path)
        path, tail = os.path.split(path)

    return paths


def update_path(path, item):
    """Update path with new item"""
    if item == '..':
        path = os.path.dirname(path)
    else:
        path = os.path.join(path, item)

    return path


def has_parent(path):
    """Check if a path has a parent folder"""
    return os.path.basename(path) != ''


def get_dir_contents(path, hidden=False, include_files=True, include_folders=True, include_drives=True):
    """Get directory contents"""
    files = list()
    dirs = list()
    drives = list()

    if os.path.isdir(path):
        for item in os.listdir(path):
            append = True
            if item.startswith('.') and not hidden:
                append = False
            full_item = os.path.join(path, item)
            if os.path.isdir(full_item) and append and include_folders:
                dirs.append(item)
            elif append and include_files:
                files.append(item)
        if has_parent(path) and include_folders:
            dirs.insert(0, '..')
        if not has_parent(path) and include_folders and include_drives:
            drives = get_drive_letters()
    return sorted(drives) + sorted(dirs) + sorted(files)


def get_drive_letters():
    import sys
    if sys.platform == "win32":
        # Windows has letters
        import string
        from ctypes import windll
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(letter + ":\\")
            bitmask >>= 1
        return drives
    else:
        # Unix does not have letters
        return []


