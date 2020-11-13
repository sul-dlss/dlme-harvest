#!/usr/bin/python
import glob, os, requests
import pandas as pd

def main():
    directory = "output/american-numismatic-society/data/"
    os.makedirs(os.path.dirname(directory), exist_ok=True)

    record_number = 1
    for i in range(1, 9):
        url = "http://numismatics.org/search/query.csv?q=imagesavailable:true%20AND%20department_facet:%22Islamic%22&start={}".format(record_number)
        data = requests.get(url, allow_redirects=True)
        open('{}{}.csv'.format(directory, i), 'wb').write(data.content)
        record_number += 1000

    csv_files = glob.glob("{}*.csv".format(directory))
    combined_csv = pd.concat([pd.read_csv(f) for f in csv_files])
    combined_csv.to_csv( "{}american-numismatic-society.csv".format(directory), index=False, encoding='utf-8-sig')

    for f in csv_files:
        os.remove(f)

if __name__ == "__main__":
    main()
