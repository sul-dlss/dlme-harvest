import urllib.request
import csv

reader = csv.DictReader(open('/Users/jtim/Desktop/near-eastern-20181028.csv', 'r'), delimiter=",")
out_file = open('../output/near-eastern-20181028.csv', 'w')

for row in reader:
    writer = csv.DictWriter(out_file, next(reader))
    try:
        url = row['url']
        response = urllib.request.urlopen(url)
        html = response.read().decode('utf-8')
        if "https://upmaa-pennmuseum.netdna-ssl.com/collections/images/image_not_available_300.jpg" not in html:
            writer.writerow(row)
    except:
        print("timeout")

out_file.close()
