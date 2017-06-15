__author__ = 'sebas'
import re
import os
import errno

def get_folder_name(name):
    return re.sub(re.compile('[^0-9a-zA-Z]+'), '_', name).lower()


def create_folder_with_path(path):
    if not os.path.exists(os.path.abspath(path)):
        try:
            os.makedirs(os.path.abspath(path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    return path

def create_folder(path, name=None):
    if (name!=None):
        target = '%s/%s' % (path, name)
    else:
        target=path

    return create_folder_with_path(target)
