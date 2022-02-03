import glob
from datetime import datetime
from pathlib import Path

for name in glob.glob('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/output/*.ndjson'):
    out_path = f"output/dlme-sample-data-{datetime.today().strftime('%Y-%m-%d')}.ndjson"
    Path(out_path).touch(exist_ok=True)
    with open(name, 'r') as file:
        with open(out_path, 'a') as out:
            for line in file.readlines():
                out.writelines(line)
