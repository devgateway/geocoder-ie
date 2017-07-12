import re
import os
import errno


def get_folder_name(name):
    return re.sub(re.compile('[^0-9a-zA-Z]+'), '_', name).lower()


def create_folder(path):
    if not os.path.exists(os.path.abspath(path)):
        try:
            os.makedirs(os.path.abspath(path))

        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    return path


