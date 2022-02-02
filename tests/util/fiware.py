import json
from typing import Optional
from uri import URI

from anomaly_detection.util.http.jclient import JsonClient
from anomaly_detection.util.ngsi.headers import FiwareContext
from anomaly_detection.util.ngsi.orion import OrionClient


TENANT = 'csic'
ORION_EXTERNAL_BASE_URL = 'http://localhost:1026'
ANOMALY_INTERNAL_BASE_URL = 'http://anomaly:8000'
QUANTUMLEAP_INTERNAL_BASE_URL = 'http://quantumleap:8668'
QUANTUMLEAP_EXTERNAL_BASE_URL = 'http://localhost:8668'
ANOMALY_DETECTOR_SUB = {
    "description": "Notify Anomaly Detector of changes to any entity.",
    "subject": {
        "entities": [
            {
                "idPattern": ".*"
            }
        ]
    },
    "notification": {
        "http": {
            "url": f"{ANOMALY_INTERNAL_BASE_URL}/updates"
        }
    }
}
QUANTUMLEAP_SUB = {
    "description": "Notify QuantumLeap of changes to any entity.",
    "subject": {
        "entities": [
            {
                "idPattern": ".*"
            }
        ]
    },
    "notification": {
        "http": {
            "url": f"{QUANTUMLEAP_INTERNAL_BASE_URL}/v2/notify"
        }
    }
}


def orion_client(service_path: Optional[str] = None,
                 correlator: Optional[str] = None) -> OrionClient:
    base_url = URI(ORION_EXTERNAL_BASE_URL)
    ctx = FiwareContext(service=TENANT, service_path=service_path,
                        correlator=correlator)
    return OrionClient(base_url, ctx)


class SubMan:

    def __init__(self):
        self._orion = orion_client()

    def create_anomaly_detector_sub(self):
        self._orion.subscribe(ANOMALY_DETECTOR_SUB)

    def create_quantumleap_sub(self):
        self._orion.subscribe(QUANTUMLEAP_SUB)

    def create_subscriptions(self) -> [dict]:
        self.create_anomaly_detector_sub()
        self.create_quantumleap_sub()
        return self._orion.list_subscriptions()

# NOTE. Subscriptions and FIWARE service path.
# The way it behaves for subscriptions is a bit counter intuitive.
# You'd expect that with a header of 'fiware-servicepath: /' Orion would
# notify you of changes to *any* entities in the tree, similar to queries.
# But in actual fact, to do that you'd have to omit the service path header,
# which is what we do here. Basically the way it works is that if you
# specify a service path, then Orion only considers entities right under
# the last node in the service path, but not any other entities that might
# sit further down below. E.g. if your service tree looks like (e stands
# for entity)
#
#                        /
#                     p     q
#                  e1   r     e4
#                     e2 e3
#
# then a subscription with a service path of '/' won't catch any entities
# at all whereas one with a service path of '/p' will consider changes to
# e1 but not e2 nor e3.


def create_subscriptions():
    print(
        f"Creating catch-all {TENANT} entities subscription for QuantumLeap.")
    print(
        f"Creating catch-all {TENANT} entities subscription for Roughnator.")

    man = SubMan()
    orion_subs = man.create_subscriptions()
    formatted = json.dumps(orion_subs, indent=4)

    print("Current subscriptions in Orion:")
    print(formatted)


class QuantumLeapEndpoints:

    def __init__(self, base_url: URI):
        self._base_url = base_url

    def _append(self, rel_path: str) -> URI:
        abspath = self._base_url.path / rel_path
        return self._base_url / abspath

    def attribute(self, entity_id: str, attr_name: str,
                  query: dict = None) -> str:
        rel_path = f"v2/entities/{entity_id}/attrs/{attr_name}"
        url = self._append(rel_path)
        if query:
            url.query = query
        return str(url)

    def entity_type(self, etype: str, attr_name: str,
                    query: dict = None) -> str:
        rel_path = f"v2/types/{etype}/attrs/{attr_name}"
        url = self._append(rel_path)
        if query:
            url.query = query
        return str(url)


class QuantumLeapClient:

    def __init__(self, base_url: URI, ctx: FiwareContext):
        self._urls = QuantumLeapEndpoints(base_url)
        self._ctx = ctx
        self._http = JsonClient()

    def time_series(self, entity_id: str, attr_name: str,
                    query: dict = None) -> dict:
        url = self._urls.attribute(entity_id, attr_name, query)
        return self._http.get(url=url, headers=self._ctx.headers())

    def all_time_series(self, entity_type: str, attr_name: str,
                        query: dict = None) -> dict:
        url = self._urls.entity_type(entity_type, attr_name, query)
        return self._http.get(url=url, headers=self._ctx.headers())


def quantumleap_client() -> QuantumLeapClient:
    base_url = URI(QUANTUMLEAP_EXTERNAL_BASE_URL)
    ctx = FiwareContext(service=TENANT, service_path='/')  # (*)
    return QuantumLeapClient(base_url, ctx)
# NOTE. Orion handling of empty service path. We send Orion entities w/ no
# service path in our tests. But when Orion notifies QL, it sends along a
# root service path. So we add it to the context to make queries work.
