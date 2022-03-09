#!/usr/bin/python
from argparse import ArgumentParser
from collections import Counter
from datetime import datetime
import json, validators

# constants
ALL_FIELDS = ['agg_data_provider_collection',
              'agg_data_provider_collection_id',
              'agg_data_provider_country',
              'agg_is_shown_by',
              'agg_preview',
              'agg_provider_country',
              'cho_alternate',
              'cho_contributor',
              'cho_coverage',
              'cho_creator',
              'cho_date',
              'cho_dc_rights',
              'cho_description',
              'cho_edm_type',
              'cho_extent',
              'cho_format',
              'cho_has_part',
              'cho_has_type',
              'cho_identifier',
              'cho_is_part_of',
              'cho_language',
              'cho_medium',
              'cho_provenance',
              'cho_publisher',
              'cho_relation',
              'cho_same_as',
              'cho_spatial',
              'cho_source',
              'cho_subject',
              'cho_temporal',
              'cho_title',
              'cho_type',
              'cho_type_facet',
              'dlme_source_file']

LANG_AWARE_FIELDS = ['agg_data_provider_collection',
                     'cho_alternate',
                     'cho_contributor',
                     'cho_coverage',
                     'cho_creator',
                     'cho_date',
                     'cho_dc_rights',
                     'cho_description',
                     'cho_has_part',
                     'cho_edm_type',
                     'cho_extent',
                     'cho_format',
                     'cho_has_type',
                     'cho_is_part_of',
                     'cho_language',
                     'cho_medium',
                     'cho_provenance',
                     'cho_publisher',
                     'cho_spatial',
                     'cho_subject',
                     'cho_title',
                     'cho_type',
                     'cho_type_facet']

# get object counts
field_counts = Counter()

def is_arabic(value):
    return True

def is_latin(value):
    return True

def is_hebrew(value):
    return True

# accesses counter object containing aggregate field counts and determines if field has been fully normalized.
# @param the field containing the raw data and the field containing the normalized data.
# returns a boolean value.
def is_normalized(raw_data_field, normalized_field):
    return field_counts[raw_data_field] == field_counts[normalized_field]

# accesses fields in individual json records and determines if they have been translated.
# @param the field in the json file.
# returns a boolean value.
def is_translated(field):
    return 'en' in field and 'ar-Arab' in field

def main():
    with open(args.file, "r") as f:
        blank_lines = []
        invalid_json = []
        json_objects = []
        ir = f.readlines()
        for count, line in enumerate(ir, start=1):
            if len(line) == 1:
                blank_lines.append(count)
            else:
                try:
                    json_objects.append(json.loads(line))
                except ValueError as e:
                    invalid_json.append(f"Line {count} does not contain valid json.")

    writepath = f"output/mapping_validation_{args.file.split('/')[-1].split('-')[-1].split('.')[0]}_{datetime.today().strftime('%Y-%m-%d')}.txt"
    with open(writepath, 'w+') as out:
        out.write("JSON VALIDATION\n")
        out.write(f"\nThere were {len(blank_lines)} blank lines in the intermediate representation.\n")
        if len(blank_lines) > 0:
            out.write(f"\nThe blank lines were: {blank_lines}\n")
        out.write(f"\nThere were {len(invalid_json)} invalid json objects in the intermediate representation.\n")
        out.write('\n---------------------------------------------------------------------------------------\n\n')
        if len(invalid_json) > 0:
            out.write(f"Lines with invalid json:\n")
            for i in invalid_json:
                out.write(f"\n\t-{i}\n")
            out.write('\n---------------------------------------------------------------------------------------\n\n')

        # language tags
        missapplied_lang_tags = []

        # date valiables
        unnormalized_dates = []
        unconverted_dates = []

        # language variables
        unnormalized_languages = []
        untranslated_languages = []

        # type variables
        unnormalized_edm_type = []
        unnormalized_has_type = []
        unnormalized_type_facet = []
        untranslated_edm_type = []
        untranslated_has_type = []
        untranslated_type_facet = []

        # url variables
        invalid_thumbnails = []
        invalid_resources = []
        missing_thumbnails = []
        missing_resources = []
        for record in json_objects:
            for field in record:
                field_counts.update({field : 1})
                if field in LANG_AWARE_FIELDS:
                    for k,v in record[field].items():
                        if '-Arab' in k:
                            if not is_arabic(k):
                                missapplied_lang_tags.append(f"Check the '*{k}' lang code in {field} in {record['id']}. The lang tag may not be correct.")
                        if k == 'he':
                            if not is_hebrew(record[field]['he']):
                                missapplied_lang_tags.append(f"Check the 'he' lang code in {field} in {record['id']}. The lang tag may not be correct.")
                        if k == 'en':
                            if not is_latin(record[field]['en']):
                                missapplied_lang_tags.append(f"Check the 'en' lang code in {field} in {record['id']}. The lang tag may not be correct.")
                        if k == 'fr':
                            if not is_latin(record[field]['fr']):
                                missapplied_lang_tags.append(f"Check the 'fr' lang code in {field} in {record['id']}. The lang tag may not be correct.")
                        if k == 'und-Latn':
                            if not is_latin(record[field]['und-Latn']):
                                missapplied_lang_tags.append(f"Check the 'und-Latn' lang code in {field} in {record['id']}. The lang tag may not be correct.")

            # date validation: checks that cho_date has been fully normalized and that all gregorian dates are converted to hijri.
            if 'cho_date' in record:
                if 'cho_date_range_norm' in record:
                    if 'cho_date_range_hijri' not in record:
                        unconverted_dates.append(f"\n\t-id: {record['id']} has normalized dates that haven't been converted to the Hijri calendar. The Gregorian date values was: {record['cho_date_range_norm']}\n")
                else:
                    unnormalized_dates.append(f"\n\t-id: {record['id']} has unnormalized dates. The raw date values was: {record['cho_date']}\n")

            # language validation: checks that cho_language has been fully normalized and translated.
            if 'cho_language' in record:
                for i in record['cho_language']['en']:
                    if i == i.lower():
                        unnormalized_languages.append({i})
                if not is_translated(record['cho_language']):
                    untranslated_languages.append(f"\n\t-id: {record['id']} has untranslated languages. Check the config file and translation maps for missing values.\n")

            # type validation: checks that cho_edm_type and cho_has_type have the same number of values,
            # that both are fully normalized, and fully translated.
            if 'cho_edm_type' in record:
                if record['cho_edm_type']['en'][0] == record['cho_edm_type']['en'][0].lower():
                    unnormalized_edm_type.append({record['cho_edm_type']['en']})
                if not is_translated(record['cho_edm_type']):
                    untranslated_edm_type.append(f"\n\t-id: {record['id']} has untranslated EDM type values. Check the config file and translation maps for {record['cho_edm_type']['en']}.\n")
                # for i in record['cho_edm_type']['en']:
                #     if 'cho_type_facet' in record:
                #         if i not in record['cho_type_facet']['en']:
                #             unnormalized_type_facet.append(f"\n\t-id: {record['id']} has unnormalized cho_type_facet values. cho_edm_type {record['cho_edm_type']['en']} and cho_type_facet = {record['cho_type_facet']['en']}.\n")
                #     else:
                #         unnormalized_type_facet.append(f"\n\t-id: {record['id']} has no cho_type_facet values. cho_type = {record['cho_type']['en']}, cho_edm_type = {record['cho_edm_type']['en']}.\n")
                if 'cho_has_type' in record:
                    if record['cho_has_type']['en'][0] == record['cho_has_type']['en'][0].lower():
                        unnormalized_has_type.append({record['cho_has_type']['en']})
                    if not is_translated(record['cho_has_type']):
                        untranslated_has_type.append(f"\n\t-id: {record['id']} has untranslated has_type values. Check the config file and translation maps for {record['cho_has_type']['en']}.\n")
                    if 'cho_type_facet' in record:
                        facet_values = []
                        for f in record['cho_type_facet']['en']:
                            facet_values.append(f.split(':')[-1])
                        for i in record['cho_has_type']['en']:
                            if i not in facet_values:
                                unnormalized_type_facet.append(f"\n\t-id: {record['id']} has unnormalized cho_type_facet values. cho_has_type = {record['cho_has_type']['en']} and cho_type_facet = {record['cho_type_facet']['en']} .\n")
                    else:
                        unnormalized_type_facet.append(f"\n\t-id: {record['id']} has no cho_type_facet values. cho_type = {record['cho_type']['en']}, cho_has_type = {record['cho_has_type']['en']}.\n")
            if 'cho_type_facet' in record:
                if not is_translated(record['cho_type_facet']):
                    untranslated_type_facet.append(f"\n\t-id: {record['id']} has untranslated has type facet vlaues. Check the config file and translation maps for missing values.\n")
                if 'cho_has_type' not in record:
                    unnormalized_type_facet.append(f"This raw type value did not make it through the chain of translation maps: {record['cho_type']}")
                if 'cho_edm_type' not in record:
                    unnormalized_type_facet.append(f"This raw type value did not make it through the chain of translation maps: {record['cho_type']}")



            # url validation: checks for missing or invalid urls in the agg_preview and agg_is_shown_at fields.
            if 'agg_preview' in record:
                valid=validators.url(record['agg_preview']['wr_id'])
                if valid==True:
                    pass
                else:
                    invalid_thumbnails.append(f"\n\t-id: {record['id']} \n\t  url: {record['agg_preview']['wr_id']} \n")
            else:
                missing_thumbnails.append(f"\n\t-id: {record['id']} is missing thumbnails.\n")

            if 'agg_is_shown_at' in record:
                valid=validators.url(record['agg_is_shown_at']['wr_id'])
                if valid==True:
                    pass
                else:
                    invalid_resources.append(f"\n\t-id: {record['id']} \n\t  url: {record['agg_is_shown_at']['wr_id']} \n")
            else:
                missing_resources.append(f"\n\t-id: {record['id']} is missing resource urls.\n")

        # write field mapping validation
        out.write("FIELD MAPPING VALIDATION\n")
        out.write("\nThe following fields have not been mapped:\n" )
        for i in ALL_FIELDS:
            if i not in field_counts:
                out.write(f"\n\t-{i}\n")
        out.write('\n---------------------------------------------------------------------------------------\n\n')

        # write date validation results
        out.write("DATE NORMALIZATION\n")
        if not is_normalized('cho_date', 'cho_date_range_norm'):
            out.write("\ncho_date and cho_date_range_norm appear to have a different number of values. The date values have not been fully normalized. Check the traject config code and the date values. The macro used to parse the dates may not be parsing some of them. Also make sure that the source data for cho_date is the same as cho_date_range_norm.\n" )
        out.write(f"\nThere were {len(unnormalized_dates)} unnormalized dates:\n")
        for i in unnormalized_dates:
            out.write(i)
        out.write(f"\nThere were {len(unconverted_dates)} Gregorian dates that were not converted to the Hijri calendar.\n")
        for i in unconverted_dates:
            out.write(i)
        out.write('\n---------------------------------------------------------------------------------------\n\n')

        # write language validation results
        out.write("LANGUAGE NORMALIZATION AND TRANSLATION\n")
        if len(unnormalized_languages) > 0:
            out.write('Consider adding these values to the translation maps:')
            for i in unnormalized_languages:
                out.write(f"\n\t-{i}\n")
        else:
            out.write('\nAll language values have been normalized.\n')
        if len(untranslated_languages) > 0:
            out.write('\nAdd these values to the Arabic translation map:')
            for i in untranslated_languages:
                out.write(f"\n\t-{i}\n")
        else:
            out.write('\nAll language values have been translated.\n')
        out.write('\n---------------------------------------------------------------------------------------\n\n')

        # write type validation results
        out.write("TYPE NORMALIZATION AND TRANSLATION\n\n")
        if not is_normalized('cho_edm_type', 'cho_has_type'):
            out.write(f"\ncho_edm_type has {field_counts['cho_edm_type']} and cho_has_type has {field_counts['cho_has_type']} values. The type values have not been fully normalized. Check the traject config code and the translation maps.\n" )
        if not is_normalized('cho_edm_type', 'cho_type_facet'):
            out.write(f"\ncho_edm_type has {field_counts['cho_edm_type']} and cho_type_facet has {field_counts['cho_type_facet']} values. The type values have not been fully normalized. Check the traject config code and the translation maps.\n" )
        if not is_normalized('cho_has_type', 'cho_type_facet'):
            out.write(f"\ncho_has_type has {field_counts['cho_has_type']} and cho_type_facet has {field_counts['cho_type_facet']} values. The type values have not been fully normalized. Check the traject config code and the translation maps.\n" )
        if len(unnormalized_edm_type) > 0:
            out.write('\nConsider adding these values to the translation maps:\n')
            for i in unnormalized_edm_type:
                out.write(f"\n\t-{i}\n")
        else:
            out.write('\nAll EDM type values have been normalized.\n')
        if len(untranslated_edm_type) > 0:
            out.write('Add these values to the Arabic translation map called with cho_edm_type:')
            for i in untranslated_edm_type:
                out.write(f"\n\t-{i}\n")
        else:
            out.write('\nAll EDM type values have been translated.\n')
        if len(unnormalized_has_type) > 0:
            out.write('Consider adding these values to the translation maps:')
            for i in unnormalized_has_type:
                out.write(f"\n\t-{i}\n")
        else:
            out.write('\nAll has type values have been normalized.\n')
        if len(untranslated_has_type) > 0:
            out.write('Add these values to the Arabic translation map called with cho_has_type:')
            for i in untranslated_has_type:
                out.write(f"\n\t-{i}\n")
        else:
            out.write('\nAll has type values have been translated.\n')
        if len(unnormalized_type_facet) > 0:
            out.write('\nCondsider adding the following cho_type_facet values to a translation map:\n')
            for i in unnormalized_type_facet:
                out.write(f"\n\t-{i}\n")
        if len(untranslated_type_facet) > 0:
            out.write('\nAdd these values to the Arabic translation map called with cho_type_facet:')
            for i in untranslated_edm_type:
                out.write(f"\n\t-{i}\n")
        else:
            out.write('\nAll type facet values have been translated.\n')
        out.write('\n---------------------------------------------------------------------------------------\n\n')

        # write url validation results
        out.write("URL VALIDATION\n")
        out.write(f"\nThere were {len(invalid_thumbnails)} invalid thumbnail urls.\n")
        for i in invalid_thumbnails:
            out.write(i)
        out.write(f"\nThere were {len(invalid_resources)} invalid resource urls.\n")
        for i in invalid_resources:
            out.write(i)
        out.write(f"\nThere were {len(missing_thumbnails)} invalid thumbnail urls.\n")
        for i in missing_thumbnails:
            out.write(i)
        out.write(f"\nThere were {len(missing_resources)} invalid resource urls.\n")
        for i in missing_resources:
            out.write(i)
        out.write('\n---------------------------------------------------------------------------------------\n\n')

        # write url validation results
        out.write("BCP47 LANG CODE VALIDATION\n\n")
        if len(missapplied_lang_tags) > 0:
            out.write('The following records may have missapplied lang tags:\n')
            for i in missapplied_lang_tags:
                out.write(f"\n\t-{i}\n")
        else:
            out.write("All lang tags seem to have the correct script.\n")
        out.write('\n---------------------------------------------------------------------------------------\n\n')

if __name__ == "__main__":
    # CLI client options.
    parser = ArgumentParser()

    parser.add_argument(
        "file",
        nargs="?",
        help="Which file do you want to validate?")

    args = parser.parse_args()
    main()
