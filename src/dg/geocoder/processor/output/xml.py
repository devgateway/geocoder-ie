import os


def save_to_xml(out_file, activity_reader, out_path=''):
    activity_reader.save(os.path.realpath(os.path.join(out_path, out_file)))
