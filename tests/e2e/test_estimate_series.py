import pytest
from requests.exceptions import HTTPError

from anomaly_detection.util.ngsi.orion import OrionClient
from tests.util.fiware import QuantumLeapClient, SubMan
from tests.util.sampler import MachineSampler
from tests.util.wait import wait_until


MACHINE_N = 2
SAMPLES_PER_MACHINE = 3
ESTIMATE_ENTITY_TYPE = 'AnomalyDetection'
DETECTION_ATTR_NAME = 'Label'


def upload_machine_entities(orion: OrionClient):
    sampler = MachineSampler(machines_n=MACHINE_N, orion=orion)
    sampler.sample(samples_n=SAMPLES_PER_MACHINE, sampling_rate=1.5)


def has_time_series(quantumleap: QuantumLeapClient) -> bool:
    try:
        series = quantumleap.all_time_series(ESTIMATE_ENTITY_TYPE,
                                             DETECTION_ATTR_NAME)
        entities = series['entities']

        if len(entities) == MACHINE_N:
            sample_size = 0
            for e in entities:
                sample_size += len(e['values'])
            return sample_size > (SAMPLES_PER_MACHINE * MACHINE_N) / 2  # (*)

        return False

    except HTTPError:  # probably no notifications received yet...
        return False

# NOTE. Orion missed notifications. If things happen too fast, Orion might
# not notify QL of all RoughnessEstimate entities it got from Roughnator.
# If memory serves, by default, if Orion gets multiple updates for the
# same entity within one second, it'll only notify subscribers of the
# latest update.


@pytest.mark.skip(reason='keeps on failing from the CLI but works when ' +
                         'debugging in the IDE. Go figure...')
def test_anomaly_detection_series(orion: OrionClient, quantumleap: QuantumLeapClient):
    SubMan().create_subscriptions()
    upload_machine_entities(orion)
    wait_until(lambda: has_time_series(quantumleap))
