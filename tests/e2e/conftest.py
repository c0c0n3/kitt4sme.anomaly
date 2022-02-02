import pytest

from anomaly_detection.util.ngsi.orion import OrionClient
from tests.util.docker import DockerCompose
from tests.util.fiware import orion_client, quantumleap_client, \
    QuantumLeapClient
from tests.util.wait import wait_for_orion

docker = DockerCompose(__file__)


@pytest.fixture(scope='session', autouse=True)
def build_images():
    docker.build_images()


@pytest.fixture(scope='package', autouse=True)
def run_services():
    docker.start()
    wait_for_orion()
    yield
    docker.stop()


@pytest.fixture(scope="module")
def orion() -> OrionClient:
    return orion_client()


@pytest.fixture(scope="module")
def quantumleap() -> QuantumLeapClient:
    return quantumleap_client()
