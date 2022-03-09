# !/usr/bin/python

import os
import ndjson
import glob

sample_files = []

# for root, dirs, files in os.walk("/Users/jtim/Dropbox/DLSS/DLME/dlme-metadata/", topdown=False):
#     files = [f for f in files if not f[0] == '.']
#     dirs[:] = [d for d in dirs if not d[0] == '.']
#     for name in files[0:5]:
#         if name.split('.')[-1] in ['csv', 'xml', 'json']:
#             sample_files.append((os.path.join(root, name)))
#
# for file in sample_files:
#     directory = '/'.join(file.split('/')[:-1]).replace('dlme-metadata', 'dlme-metadata-data-sample')
#     os.makedirs(directory, exist_ok=True)
#     shutil.copy(file, f"{file.replace('dlme-metadata', 'dlme-metadata-data-sample')}")
with open('dlme-sample-data-march-03-2022.ndjson', 'w') as out:
    # writer = ndjson.writer(out, ensure_ascii=False)

    for file in glob.glob("/Users/jtim/Downloads/*ndjson"):
        with open(file, 'r') as input:
            for line in input.readlines()[0:5]:
                # data = ndjson.loads(line)
                out.write(line)
                # print(data)
            # writer.writerow(line)


# with open('dlme-sample-data-march-03-2022.ndjson', 'w') as f:
#     for file in sample_files:
#         ndjson.dump(file, f)
#         directory = '/'.join(file.split('/')[:-1]).replace('dlme-metadata', 'dlme-metadata-data-sample')
#         os.makedirs(directory, exist_ok=True)
#         shutil.copy(file, f"{file.replace('dlme-metadata', 'dlme-metadata-data-sample')}")

# Make sure all output files were removed
# for root, dirs, files in os.walk("/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/output/", topdown=False):
#     files = [f for f in files if not f[0] == '.']
#     assert len(files) == 0
