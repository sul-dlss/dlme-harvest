# !/usr/bin/python

import os
import shutil

sample_files = []

for root, dirs, files in os.walk("/Users/jtim/Dropbox/DLSS/DLME/dlme-metadata/", topdown=False):
    files = [f for f in files if not f[0] == '.']
    dirs[:] = [d for d in dirs if not d[0] == '.']
    for name in files[0:5]:
        if name.split('.')[-1] in ['csv', 'xml', 'json']:
            sample_files.append((os.path.join(root, name)))

for file in sample_files:
    directory = '/'.join(file.split('/')[:-1]).replace('dlme-metadata', 'dlme-metadata-data-sample')
    os.makedirs(directory, exist_ok=True)
    shutil.copy(file, f"{file.replace('dlme-metadata', 'dlme-metadata-data-sample')}")

for root, dirs, files in os.walk("/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/output/", topdown=False):
    files = [f for f in files if not f[0] == '.']
    for name in files:
        os.remove(os.path.join(root, name))

# Make sure all output files were removed
for root, dirs, files in os.walk("/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/output/", topdown=False):
    files = [f for f in files if not f[0] == '.']
    assert len(files) == 0
