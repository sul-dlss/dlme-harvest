# How To Add Data to DLME from a New Provider

When adding data to DLME from a new data provider, there are several areas of multiple codebases that must be updated. In this document, we walk through all the necessary steps and link to examples to help clarify the process.

This process leverages extensions to [Traject, a configuration-based MARC to Solr indexer written in Ruby](https://github.com/traject/traject). We have extended it to provide configuration-based conversion from your data source (as XML, CSV, JSON, or binary MARC21) to the DLME MAP represented in JSON. Configuration-based conversion means each data from a new provider creates a new configuration file to indicate their mappings and any fixed fields for the dataset. The mappings in the configurations are meant to be as simple as possible so that providers don't need to be Ruby programmers to write these. To read more about our extensions to Traject for this data pipeline, you can read our [Traject Extensions documentation](extensions_to_traject.md).

## Steps

1. [Load Your Metadata into Our DLME Metadata GitHub Repository](#1-stage-your-metadata)
2. [Create a Branch on This GitHub Repository](#2-create-a-dlme-github-repository-branch)
3. [Add Your Data Source's Settings](#3-add-your-data-source-settings)
4. [Establish data mapping](#4-create-your-data-mapping)
5. [Write mapping configuration](#5-create-your-mapping-configuration-file)
6. [Optional: Write mapping macro for data transformations](#6-mapping-macros)
7. [Write spec to test data mapping and provide fixture data for testing](#7-test-your-data-mapping)
8. [Create Your Pull Request](#8-create-a-pull-request)

## 1. Stage Your Metadata

At present, this DLME prototype loads metadata from this DLME Metadata GitHub repository: https://github.com/sul-dlss/dlme-metadata. You will need to add your metadata - in the appropriate directory - via a pull request to that DLME Metadata GitHub repository for it to be loaded by our pipeline.

## 2. Create a DLME GitHub Repository Branch

With your metadata staged in the [DLME Metadata GitHub repository](https://github.com/sul-dlss/dlme-metadata), you now need prepare a branch - to then become a pull request when you're done - on this DLME application GitHub repository. This branch will add your new data source configuration, update the loading settings to load your new metadata, add a data conversion test for your new metadata mapping, and add any other optional code for your new data conversion.

## 3. Add Your Data Source Settings

You need to update the https://github.com/sul-dlss/dlme-traject/blob/master/metadata_mapping.json file for this application codebase to include information for the new data source. To do so:

1. At the end of the sources section in https://github.com/sul-dlss/dlme-traject/blob/master/metadata_mapping.json, following the existing format (see the example below).
2. Give it a meaningful and unique data source name: `stanford_mods:` or `my_new_source:`.
3. Indicate the directory within the [DLME metadata repository](https://github.com/sul-dlss/dlme-metadata) where your metadata files are located.
4. If your metadata is in only 1 file within the DLME Metadata repository directory indicated, used the optional regex lookup: `only: !ruby/regexp '/egyptian-20170820.csv/'`
5. Indicate the name of your mapping's Traject configuration file (you create this file in the next step): `traject_file: my_new_source_config`
6. Assign any appropriate, static properties for your metadata. Example:
```
`agg_provider`: Stanford University
`inst_id`: short id prefix [i.e. `my_source` or `stanford_mods`]
```

### Example configuration

```json
[
  {
   "trajects": [
     "mods_config.rb"
   ],
   "paths": [
     "stanford/maps"
   ],
   "extension": ".mods",
   "settings": {
     "agg_provider": "Stanford Libraries",
     "agg_data_provider": "Stanford Libraries",
     "inst_id": "stanford"
   }
  }
]
```

__paths__: The directory for the data in GitHub dlme-metadata repo ; required
__extension__: File extension of the types of files to important ; optional
__trajects__: The Traject Mapping config file found in the GitHub dlme-traject repo ; required
__settings__: Settings for the data import source ; required
  __agg_provider__: Who delivered the data directly to DLME ; required
    agg_provider: Stanford University Libraries
    # Who created the data originally ; optional
    agg_data_provider: Stanford Geospatial Library
    # Prefixes the solr document ID ; optional
    inst_id: stanford_mods


## 4. Create Your Data Mapping

Metadata ingested into the DLME needs to be mapped to the DLME Metadata Application Profile (MAP), or the available classes, fields, and definitions (including requirements) for objects described in DLME. You can read more details on the [DLME MAP at this link.](application_profile.md)

You need to write a mapping from your provided metadata to our DLME MAP. You need to pay special attention to the required fields (identifier, title, language if applicable and URL to view the object). To get started, you can view existing mappings or add your own mapping to our [open DLME Mappings Google spreadsheet.](https://docs.google.com/spreadsheets/d/1Sp7uMHizVX7xN7xN9mm-vgEuESQBovXO-qenAo_TV-w/edit) Where possible, map DLME field names as found in the DLME spreadsheet tab to XPath, Objectpath (for JSON), headers for columns (if CSV), or MARC fields (if MARC) - this will ease the configuration writing process (the next step).

You do not need to add to this mapping spreadsheet, but it can help with writing your configuration in the next step, as well as help future mappings by leaving behind examples.

## 5. Create Your Mapping Configuration File

The following instructions are based on the original documentation for [Traject](https://github.com/traject/traject), the tool we use and expand in our DLME data pipeline.

Start by creating a new file in the [dlme-traject repo](https://github.com/sul-dlss/dlme-metadata) named for the source as referenced above in step 3 (e.g. `my_new_source_config.rb` or `stanford_mods.rb` - whatever you put as your name for the `traject_file` field above in https://github.com/sul-dlss/dlme-traject/blob/master/metadata_mapping.json).

You then add your mapping using the Traject DSL (domain specific language), which simplifies the expected mapping for records in your metadata. Below are starting examples for mapping configuration files, with further links for examples, available DSL extensions for the formats, and other information.

### Mapping CSV Data

All CSV configurations must have the following at the top of your configuration file:

```
require_relative 'csv_reader'
require_relative 'dlme_json_resource_writer'
require_relative 'macros/dlme'
require_relative 'macros/extraction'
require_relative 'macros/csv'
extend Macros::DLME
extend Macros::Csv

settings do
  provide 'writer_class_name', 'DlmeJsonResourceWriter'
  provide 'reader_class_name', 'CsvReader'
end
```

Then, for each field in your mapping, a `to_field` command is required, like so:

```
to_field('DLME field name'), column('Your CSV column name', [OPTIONS])
```

For more help with CSVs:
- [look at generic CSV configurations here](basic_config_examples.md#comma-separated-values)
- review [this Metropolitan Museum of Art CSV configuration as an example](../lib/traject/met_csv_config.rb)

### Mapping XML Data

All XML configurations must have the following at the top of your configuration file:

```ruby
require_relative 'xml_reader'
require_relative 'dlme_json_resource_writer'
require_relative 'macros/dlme'
require_relative 'macros/extraction'
require_relative 'macros/xml'
extend Macros::DLME
extend Macros::Xml

settings do
  provide 'writer_class_name', 'DlmeJsonResourceWriter'
  provide 'reader_class_name', 'XmlReader'
end
```
Then, for each field (Xpath for the record) in your mapping, a `to_field` command is required, like so:

```ruby
to_field('DLME field name'), extract_xml(xpath [OPTIONS])
```

For specific schema (MODS, TEI, FGDC), there exist shortcuts that perform the `extract_xml` method but with specific namespaces loaded:

```ruby
to_field('DLME field name'), extract_mods(xpath [OPTIONS])
to_field('DLME field name'), extract_tei(xpath [OPTIONS])
to_field('DLME field name'), extract_fgdc(xpath [OPTIONS])
```

More help for XML files:
- [look at generic XML configurations here](basic_config_examples.md#xml)
- review [this MODS configuration as an example here](../lib/traject/mods_config.rb)
- review schema-specific XML additions in our [MODS macros](../lib/traject/macros/mods.rb), our [TEI macros](../lib/traject/macros/tei.rb), and our [FGDC macros](../lib/traject/macros/fgdc.rb).

### Mapping Binary MARC Data

All binary MARC configurations must have the following at the top of your configuration file:

```ruby
require 'traject/macros/marc21_semantics'
require 'traject/macros/marc_format_classifier'
require_relative 'dlme_json_resource_writer'
require_relative 'macros/dlme'
require_relative 'macros/dlme_marc'
require_relative 'macros/extraction'

extend Macros::DLME
extend Traject::Macros::Marc21Semantics
extend Traject::Macros::MarcFormats
extend Macros::DlmeMarc

settings do
  provide 'writer_class_name', 'DlmeJsonResourceWriter'
  provide 'reader_class_name', 'MarcReader'
end

to_field 'id', extract_marc('001', first: true) do |_record, accumulator, _context|
  accumulator.collect! { |s| "penn_#{s}" }
end
```
Then, for each MARC field and subfield in your mapping, a `to_field` command is required:

```ruby
to_field('DLME field name'), extract_marc(MARC field and subfield [OPTIONS])
```

Fields and subfields can be used or just fields can be used. Also, you can indicate multiple MARC fields in one mapping. Examples:

```ruby
to_field('cho_title'), extract_marc(245)
to_field('cho_creator'), extract_marc(100a)
to_field('cho_subject'), extract_marc(600:650)
```

For more help for MARC files:
- [read more about MARC configuration files in the original Traject Project documentation](https://github.com/traject/traject#configuration-files)
- [look at generic MARC configurations here](basic_config_examples.md#binary-marc)
- review [this Pennsylvania University MARC configuration as an example here](../lib/traject/marc_config.rb)

### Cross-Format options

There are a few options that are available across data format options.

These transforms are trigged through the options passed to the specific to_field selector for that data representation ('column' for CSV, 'extract_marc' for MARC21, and 'extract_xml' for XML):

```
to_field 'DLME Field', column('CSV Column', transform: [INPUT])
to_field 'DLME Field', extract_marc('field', transform: [INPUT])
to_field 'DLME Field', extract_mods('Xpath', transform: [INPUT])
to_field 'DLME Field', extract_fgdc('Xpath', transform: [INPUT])
to_field 'DLME Field', extract_tei('Xpath', transform: [INPUT])
to_field 'DLME Field', extract_xml('Xpath', transform: [INPUT])
```

#### append

Option: string
Purpose: Add a string to the end of each value in the result list.

```
to_field 'selected_field', column('CSV Column', append: ' , added to string')
```

#### insert

Option: string
Purpose: Inserts each value in the result to a formatted string (marked by '%s').

```
to_field 'selected_field', column('CSV Column', insert: 'Insert some text %s here.')
```

#### replace

Option: string
Purpose: Replaces all instances of a string in each value in the result list with the replacement string.

```
to_field 'selected_field', column('CSV Column', replace: ['|', ' - ')
```

#### split

**Option:** string
**Purpose:** Split the column text into an array based on the splitter string
**Note:** If any other transforms will also be run on the content, *split* should always be first.

Example:
```
to_field 'selected_field', column('CSV Column', split: '|')
```

#### transform_values

One important macro to be aware of is the provided `tranform_values` macro that is use for complex/hierarchical data structures, namely for the `agg_is_shown_at` and `agg_is_shown_by` fields.

Example:

```
to_field 'agg_is_shown_at' do |_record, accumulator, context|
  accumulator << transform_values(context,
                                  'wr_id' => [column('URI')])
end
```

#### translation map

**Option:** translation map name (name for the relevant YAML file without the file extension). Options include: `types` (for EDM type lookup) ; `marc_languages` (for language lookup).
**Purpose:** The maps the passed values to the existing translation map (either in the DLME project or in Traject natively). You can add an additional option of `default: '__passthrough__'` to indicate that the original value, if not mapped, should be passed through to the DLME object.

Example:
```
extract_mods('/*/mods:language/mods:scriptTerm', translation_map: ['marc_languages'])
extract_mods('/*/mods:language/mods:scriptTerm', translation_map: ['types', default: '__passthrough__'])
```

#### trim

**Option:** boolean
**Purpose:** When `true`, whitespace is removed from the leading and trailing edges of each value in the result list.

Example:
```
to_field 'selected_field', column('CSV Column', trim: true)
```

## 6. Create a Pull Request

After you have added your mapping configuration, updated the settings to be able to pull your metadata, added your metadata to the [dlme-metadata repository](https://github.com/sul-dlss/dlme-metadata), and done any testing needed, you want to create a pull request on this repo to add your data to the master branch.

As this DLME codebase is running continuous integration, your branch will be tested (by rubocop, rspec, coveralls). Once approved and merged into master, it automatically updates the codebase deployed to our DLME code on the production server.

At that point, you should be able to go to the DLME website and kick off a `Harvest Records` job in the DLME project dashboard. If at any point you just want to rerun the indexing, you can use the `Reprocess` button. For your selected data source, it will leverage the configuration and metadata you just added above.

## Contact information

For more information, please contact [dlme-tech-data@lists.stanford.edu](mailto:dlme-tech-data@lists.stanford.edu).
