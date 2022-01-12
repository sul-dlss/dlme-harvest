#!/usr/bin/python
import json
from argparse import ArgumentParser
from collections import Counter
from datetime import date
from PIL import Image
import requests
import validators

def thumbnail_report(image_sizes_list):
    '''Takes a list of tuples as input and outputs a thumbnail image size report.'''
    passed_rec = 0
    failed_rec = 0
    rec_size = 400

    for i in image_sizes_list:
        if i[0] >= rec_size or i[1] >= rec_size:
            passed_rec+=1
        else:
            failed_rec+=1

    return f'<li>{round((passed_rec/len(image_sizes_list))*100)}% of thumbnail images had a width or height of {rec_size} or greater.</li>'

def image_size(response):
    '''Takes an http response and returns an image size.'''
    if not isinstance(response, requests.models.Response):
        raise TypeError('The parameter passed to the image_size function is not an http response.')
    size = Image.open(response.raw).size
    return size

# validate urls
def validate_url(url):
    '''Checks if url has valid form.'''
    if not validators.url(url):
        raise f"Invalid url for {record['id']}: {url}"

# resolve urls
def resolve_url(response):
    '''Checks if url is resolvable.'''
    try:
        if response.status_code==200:
            return True
    except AttributeError:
        print('The value passed to resolve_url was not a valid url.')

# Define variables for capturing data from main
thumbnail_image_sizes = []
unresolvable_resources = []
unresolvable_thumbnails = []

def main():
    '''Captures all field value counts in counter object and writes report to html file.'''
    with open(args.input, 'r') as file:
        records = file.readlines()
        report = open(f'report_{date.today()}.html', 'a')
        ignore_fields = ['agg_data_provider', 'agg_data_provider_collection', 'agg_data_provider_country',
                         'agg_is_shown_at', 'agg_preview', 'agg_provider', 'agg_provider_country',
                         'cho_type_facet', 'dlme_collection', 'dlme_source_file', 'id', 'transform_version',
                         'transform_timestamp']

        # merge all records into single counter object and write field report
        report.write('<h2>All fields in DLME intermediate record</h2>')
        field_counter = Counter()
        value_per_field_counter = Counter()
        lang_counter = {}

        for count, record in enumerate(records, start=1):
            record = json.loads(record)
            # Get field information
            for field, metadata in record.items():
                field_counter.update({field : 1})
                if isinstance(metadata, dict):
                    for lang, values in metadata.items():
                        if lang_counter.get(field):
                            if lang_counter.get(field).get(lang):
                                lang_counter[field][lang] += 1
                            else:
                                lang_counter[field][lang] = 1
                        else:
                            lang_counter.update({field: {lang: 1}})
                        value_per_field_counter.update({field : len(values)})
                else:
                    value_per_field_counter.update({field : len(metadata)})
            if 'agg_dc_rights' in record['agg_is_shown_at']:
                field_counter.update({'agg_is_shown_at.agg_dc_rights' : 1})
            if 'agg_edm_rights' in record['agg_is_shown_at']:
                field_counter.update({'agg_is_shown_at.agg_edm_rights' : 1})
            if 'wr_dc_rights' in record['agg_is_shown_at']:
                field_counter.update({'agg_is_shown_at.wr_dc_rights' : 1})
            if 'wr_edm_rights' in record['agg_is_shown_at']:
                field_counter.update({'agg_is_shown_at.wr_edm_rights' : 1})
            if 'wr_id' in record['agg_is_shown_at']:
                field_counter.update({'agg_is_shown_at.wr_id' : 1})
            if 'wr_id' in record['agg_preview']:
                field_counter.update({'agg_preview.wr_id' : 1})
            if 'wr_is_referenced_by' in record['agg_is_shown_at']:
                field_counter.update({'agg_is_shown_at.wr_is_referenced_by' : 1})

            # Resolve resource url
            validate_url(record['agg_is_shown_at']['wr_id']) # will fail if invalid url
            resource = requests.get(record['agg_is_shown_at']['wr_id'], stream=True)
            if not resolve_url(resource):
                unresolvable_resources.append(record['agg_is_shown_at']['wr_id'])

            # Resolve thumbnail url, get size for sample of images or all
            # depending on number of records in dataset
            validate_url(record['agg_preview']['wr_id']) # will fail if invalid url
            thumbnail = requests.get(record['agg_preview']['wr_id'], stream=True)
            if not resolve_url(thumbnail):
                unresolvable_thumbnails.append(record['agg_preview']['wr_id'])
            if len(records) > 5000:
                if count%20==0:
                    thumbnail_image_sizes.append(image_size(thumbnail))
            elif len(records) > 500:
                if count%10==0:
                    thumbnail_image_sizes.append(image_size(thumbnail))
            if len(records) > 100:
                if count%2==0:
                    thumbnail_image_sizes.append(image_size(thumbnail))
            else:
                thumbnail_image_sizes.append(image_size(thumbnail))

        ignore_value_counts = ['agg_data_provider_collection', 'agg_preview', 'agg_is_shown_at', 'cho_date_range_hijri', 'cho_date_range_norm', 'transform_timestamp', 'transform_version', 'id', 'dlme_collection', 'agg_is_shown_at.wr_dc_rights']
        report.write('<ul>')
        for item, count in sorted(field_counter.items()):
            if item not in ignore_fields:
                if not isinstance(value_per_field_counter.get(item), type(None)):
                    report.write(f'<li><b>{item}</b>: {count} of {len(records)} ({round(count/len(records)*100)}%)</li>')
                    report.write('<ul>')
                    report.write(f'<li>Average number of values: {round(value_per_field_counter.get(item)/len(records), 2)}</li>')
                    if not isinstance(lang_counter.get(item), type(None)):
                        report.write(f'<li>Languages: {lang_counter.get(item)}</li>')
                    report.write('</ul>')
        report.write('</ul>')

        # DLME resource section
        report.write('<h2>DLME resource report</h2>')
        report.write('<ul>')
        report.write(f"<li>{field_counter['agg_preview.wr_id']} of {len(records)} records had valid urls to thumbnail images.</li>")
        if len(unresolvable_thumbnails) > 0:
            report.write('<li>The following thumbnails urls were unresolvable when testing:</li>')
            report.write('<ul>')
            for i in unresolvable_thumbnails:
                report.write(f'<li>{i}</li>')
            report.write('</ul>')
        report.write(f"<li>{field_counter['agg_is_shown_at.wr_id']} of {len(records)} records had valid urls to resources.</li>")
        if len(unresolvable_resources) > 0:
            report.write('<li>The following resource urls were unresolvable when testing:</li>')
            report.write('<ul>')
            for i in unresolvable_resources:
                report.write(f'<li>{i}</li>')
            report.write('</ul>')
        report.write(f"<li>{field_counter['agg_is_shown_at.wr_is_referenced_by']} of {len(records)} records had iiif manifests.</li>")
        report.write('</ul>')

        # DLME rights section
        report.write('<h2>DLME rights report</h2>')
        report.write('<ul>')
        report.write(f"<li>{field_counter['cho_dc_rights']} of {len(records)} records had a clearly expressed copyright status for the cultural heritage object.</li>")
        wr_edm = field_counter['agg_is_shown_at.wr_edm_rights']
        wr_dc = field_counter['agg_is_shown_at.wr_dc_rights']
        if wr_edm > 0:
            wr_count = wr_edm
        else:
            wr_count = wr_dc
        report.write(f'<li>{wr_count} of {len(records)} records had a clearly expressed copyright status for the web resource.</li>')
        report.write(f"<li>{field_counter['agg_edm_rights']} of {len(records)} records had clearly expressed aggregation rights.</li>")
        report.write('</ul>')

        # Thumbnail size section
        report.write(f'<h2>DLME thumbnail image quality report (a sample of {len(thumbnail_image_sizes)} images were tested).</h2>')
        report.write('<ul>')
        report.write(thumbnail_report(thumbnail_image_sizes))
        report.write('</ul>')

        report.close()

if __name__ == '__main__':
    # CLI client options.
    parser = ArgumentParser()
    parser.add_argument(
        "input",
        nargs="?",
        help="What is the file path to the intermediate representation?")
    args = parser.parse_args()
    main()
