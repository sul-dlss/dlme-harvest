#!/usr/bin/python
import backoff, json, os, requests
from argparse import ArgumentParser
from requests.adapters import TimeoutSauce
from subprocess import call

REQUESTS_TIMEOUT_SECONDS = float(os.getenv("REQUESTS_TIMEOUT_SECONDS", 4))

# Make explicit default timeout for requests calls by setting it.
class CustomTimeout(TimeoutSauce):
    def __init__(self, *args, **kwargs):
        if kwargs["connect"] is None:
            kwargs["connect"] = REQUESTS_TIMEOUT_SECONDS
        if kwargs["read"] is None:
            kwargs["read"] = REQUESTS_TIMEOUT_SECONDS
        super().__init__(*args, **kwargs)

class ServerError(requests.exceptions.HTTPError):
    pass

# Set it globally, instead of specifying ``timeout=..`` kwarg on each call.
requests.adapters.TimeoutSauce = CustomTimeout

# Re-usable decorator with exponential wait.
retry_timeout = backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(
        ServerError,
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError
    ),
    max_tries=REQUESTS_MAX_RETRIES,
)

@retry_timeout
def fetch_server_info(self, *args, **kwargs):
    resp = requests.get(SERVER_URL)
    if resp.status_code >= 500:
        raise ServerError("Boom!", response=resp)
    return resp.json()

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=REQUESTS_MAX_RETRIES)
session.mount('https://', adapter)

def harvest_sequence(institution):
    print('Harvesting {}'.format(institution))
    for script in institution['harvest']:
        __import__(script)
        call(["python", "{}.py".format(script)])
    print('Cleaning {}'.format(institution))
    for script in institution['cleanup']:
        __import__(script)
        call(["python", "{}.py".format(script)])

def main():
    with open('map.json') as map:
        data = json.load(map)
        if args.institution == 'all': # harvest all collections
            try:
                for institution in data:
                    harvest_sequence(institution)
            except:
                logger.exception('Error: Check the map.json file and your spelling; make sure there are no errors in the harvesting script.')
        else: # harvest collection specified
            try:
                for m in data:
                    if institution['inst_id'] == args.institution:
                        harvest_sequence(institution)
            except:
                logger.exception('Error: Check the map.json file and your spelling; make sure there are no errors in the harvesting script.')

if __name__ == "__main__":
    # CLI client options.
    parser = ArgumentParser()
    parser.add_argument(
        "institution",
        help="put the institution name (see harvest-mapping.json) you want harvested here.")

    args = parser.parse_args()
    main()
