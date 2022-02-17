#!/usr/bin/python
import backoff, os, requests, unittest
from requests.adapters import TimeoutSauce
from toxiproxy import Toxiproxy

REQUESTS_TIMEOUT_SECONDS = float(os.getenv("REQUESTS_TIMEOUT_SECONDS", 2))

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

REQUESTS_MAX_RETRIES = int(os.getenv("REQUESTS_MAX_RETRIES", 4))

# session = requests.Session()
# adapter = requests.adapters.HTTPAdapter(max_retries=REQUESTS_MAX_RETRIES)
# session.mount('https://', adapter)

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

# Testing
toxiserver = Toxiproxy()
toxiserver.create(name="fantastic_api_dev", upstream="localhost:8888")


class LatencyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proxy = toxiserver.get_proxy(name="fantastic_api_dev")
        cls.proxy.add_toxic(name="latency_downstream", type="latency", attributes={"latency": 500})
        cls.proxy_url = "http://" + cls.proxy.listen

    @classmethod
    def tearDownClass(cls):
        cls.proxy.destroy_toxic("latency_downstream")

    def test_client_raises_error(self):
        client = APIClient(server=self.proxy_url, timeout=100)
        with self.assertRaises():
            client.fetch_user_info()
