#!/usr/bin/python
import pandas as pd
import csv, glob, os, re, requests, zipfile
from datetime import datetime
from io import BytesIO

# Datasets
data_sets = {'egyptian-data': 'http://www.penn.museum/collections/assets/data/egyptian-csv-latest.zip',
           'near-east-data': 'http://www.penn.museum/collections/assets/data/near-eastern-csv-latest.zip'}

def get_image_url(df):
    try:
        irn = df['emuIRN']
        url = 'https://www.penn.museum/collections/object_images.php?irn={}'.format(irn)
        response = requests.get(url)
        html = response.text()
        image_url_pattern = re.compile(r'"https://upmaa-pennmuseum.netdna-ssl.com/collections/assets/.*?\"')
        image_url = re.findall(image_url_pattern, html)[0]
        df['image_url'] = image_url.replace('"', '')
    except:
        print('timeout')
    return df

def check_image(df):
    # print("Processing row {} of {}".format(i, df.shape[1]))
    try:
        url = df['url']
        response = requests.get(url)
        html = response.text
        if "https://upmaa-pennmuseum.netdna-ssl.com/collections/images/image_not_available_300.jpg" in html:
            df.drop(df.index, axis=0)
    except:
        print("timeout")

    return df


def main():
    directory = "output/penn/penn-museum/data/"
    os.makedirs(os.path.dirname(directory), exist_ok=True)

    # for key, value in data_sets.items():
    #     r = requests.get(value, allow_redirects=True)
    #     open("{}{}.zip".format(directory, key), 'wb').write(r.content)

    zip_files = glob.glob("{}*.zip".format(directory))

    for file in zip_files:
        with zipfile.ZipFile(file) as zip:
            list = zip.infolist()
            with zip.open(list[0]) as f:
                with open("{}".format(file.replace('.zip', '.csv')), 'wb') as out_file:
                    out_file.write(f.read())

    data_files = glob.glob("{}*data.csv".format(directory))

    for file in data_files:
        # with open("{}".format(file.replace('.csv', '-clean.csv')), 'w') as out_file:
        df = pd.read_csv(file)
        # Check for valid image
        df = df.apply(check_image, axis=1)
        df.to_csv("{}".format(file).replace('.csv', '-image.csv'))
        # Get image url
        # df = df.apply(get_image_url, axis=1)

        # Get thumbnail url


        # reader = csv.DictReader(open(file, 'r'), delimiter=",")
        # writer = csv.DictWriter(out_file, fieldnames=reader.fieldnames)
        # writer.writeheader()


        # for count, l in enumerate(reader):
        #     total_rows = count + 1
        #
        # print(total_rows)
        # for row in reader:
        #     try:
        #         url = row['url']
        #         response = requests.get(url)
        #         html = response.text
        #         if "https://upmaa-pennmuseum.netdna-ssl.com/collections/images/image_not_available_300.jpg" not in html:
        #             writer.writerow(row)
        #             out_file.flush() # Write csv rows from memory to file
        #             print("Processing row # {}".format(count))
        #         count += 1
        #     except:
        #         print("timeout")
        #         count += 1

        # Get image url
    # data_files_with_images = glob.glob("{}*image.csv".format(directory))
    # for file in data_files_with_images:
    #     df = pd.read_csv(file)
    #     df = df.apply(get_image_url, axis=1)



if __name__ == "__main__":
    main()
