#!/usr/bin/python
import glob, json, io, os, requests, urllib

def del_none(d):
    """
    Delete keys with the value ``None`` in a dictionary, recursively.

    This alters the input so you may wish to ``copy`` the dict first.
    """
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d  # For convenience

def main():
    directory = "/Users/jtim/Dropbox/DLSS/DLME/dlme-metadata/walters-art-museum-clean/data/"
    os.makedirs(os.path.dirname(directory), exist_ok=True)
    for count, file in enumerate(glob.glob("/Users/jtim/Dropbox/DLSS/DLME/dlme-metadata/walters-art-museum/data/*.json"), start=1):
        with open(file) as f:
            data = json.load(f)
            new_file = del_none(data)
            filename = '/Users/jtim/Dropbox/DLSS/DLME/dlme-metadata/walters-art-museum-clean/data/walters-{}.json'.format(count)
            with io.open(filename, 'w') as out_file:
                json.dump(new_file, out_file)





if __name__ == "__main__":
    main()
