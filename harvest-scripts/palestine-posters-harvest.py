#!/usr/bin/python
import csv, os, requests, time
from io import StringIO
from lxml import etree

parser = etree.HTMLParser()
page_errors = []
resource_errors = []

def main():
    directory = "output/palestine-posters/data/"
    os.makedirs(os.path.dirname(directory), exist_ok=True)

    with open("{}palestine-posters.csv".format(directory), 'w') as out_file:
        pppa_writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        pppa_writer.writerow([ 'Resource-URL', 'Thumbnail', 'Title', 'Creator', 'Date', 'Subject', 'Description'])

        def process_page(page_number):
            # Get all divs and pass to process_resource
            print("Page {} working".format(page_number))
            url = "https://www.palestineposterproject.org/list_posters?page={}".format(page_number)
            try:
                root = etree.parse(StringIO(requests.get(url).text), parser).getroot()
            except:
                print("Page error: {}".format(url))
                page_errors.append(url)
            item_divs = root.iterfind('.//div/[@class="views-field views-field-field-poster-image"]/div[@class="field-content"]/a') # find all the resources divs on each page
            for div in item_divs:
                process_resource(div)
                out_file.flush() # Write csv rows from memory to file
                time.sleep(1)

        def process_resource(element):
            # Get metadata for each div
            resource_url = "https://www.palestineposterproject.org{}".format(element.get("href"))
            try:
                metadata_root = etree.parse(StringIO(requests.get(resource_url).text), parser).getroot()
            except:
                print("Resource error: {}".format(element))
                resource_errors.append(resource_url)
            thumbnail = element.find('img[@class="image-style-medium"]').get("src")
            title = ""
            if metadata_root.find('.//meta[@name="dcterms.title"]') is not None:
                title = metadata_root.find('.//meta[@name="dcterms.title"]').get("content")
            creator = ""
            if metadata_root.find('.//meta[@name="dcterms.creator"]') is not None:
                creator = metadata_root.find('.//meta[@name="dcterms.creator"]').get("content")
            subject = ""
            if metadata_root.find('.//meta[@name="dcterms.subject"]') is not None:
                subject = metadata_root.find('.//meta[@name="dcterms.subject"]').get("content")
            description = ""
            if metadata_root.find('.//meta[@name="dcterms.description"]') is not None:
                description = metadata_root.find('.//meta[@name="dcterms.description"]').get("content")
            date = ""
            if metadata_root.find('.//meta[@name="dcterms.date"]') is not None:
                date = metadata_root.find('.//meta[@name="dcterms.date"]').get("content")

            pppa_writer.writerow([resource_url, thumbnail, title, creator, date, subject, description])

        for i in range(0, 323): # iterate over each page
            process_page(i)
        while len(page_errors) > 0: # re-process all erroneous pages
            for i in len(page_errors) + 1:
                process(page_errors.pop())
        while len(resource_errors) > 0:  # re-process all erroneous resources
            for i in len(resource_errors) + 1:
                process_resource(resource_errors.pop())

if __name__ == "__main__":
    main()
