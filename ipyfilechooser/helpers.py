import os


def get_subpaths(path):
    '''Walk a path and return a list of subpaths'''
    if os.path.isfile(path):
        path = os.path.dirname(path)

    paths = [path]
    path, tail = os.path.split(path)

    while tail:
        paths.append(path)
        path, tail = os.path.split(path)

    return paths


def update_path(path, item):
    '''Update path with new item'''
    if item == '..':
        path = os.path.dirname(path)
    else:
        path = os.path.join(path, item)

    return path


def has_parent(path):
    '''Check if a path has a parent folder'''
    return os.path.basename(path) != ''


def get_dir_contents(path, hidden=False):
    '''Get directory contents'''
    files = list()
    dirs = list()

    if os.path.isdir(path):
        for item in os.listdir(path):
            append = True
            if item.startswith('.') and not hidden:
                append = False
            full_item = os.path.join(path, item)
            if os.path.isdir(full_item) and append:
                dirs.append(item)
            elif append:
                files.append(item)
        if has_parent(path):
            dirs.insert(0, '..')
    return sorted(dirs) + sorted(files)
