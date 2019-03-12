## Harvest from the Met API.

There are two steps to getting the met data.  The first will get a list of
item identifiers.  The second step gets the metadata.

### Harvesting identifiers
We have a copy of the identifiers checked in at https://github.com/sul-dlss/dlme-harvest/blob/master/met/ancient-near-east-art/collection_identifiers.txt so you may not need this step unless you want to refresh the whole collection.
1. In your browser visit https://metmuseum.org/api/collection/collectionlisting?department=3&showOnly=openAccess, in the developer console, get the cookies, namely the one starting with `visid_incap_` and the one starting with `incap_ses_`. Update these in the COOKIES constant on line 11 of `harvest_identifiers.py`
1. `python3 harvest_identifiers.py` This produces `collection_identifiers.txt`
1. Check the updated copy into the repo.

### Harvesting metadata
This script reads from the `collection_identifiers.txt` and makes an API call for each item in the file.
1. `python3 harvest_metadata.py`
