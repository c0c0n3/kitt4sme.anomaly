import time
from typing import Callable

from tests.util.fiware import orion_client


def wait_until(action: Callable[[], bool], max_wait: float = 20.0,
               sleep_interval: float = 1.0):
    time_left_to_wait = max_wait
    while time_left_to_wait > 0:
        stop = action()
        if stop:
            return

        time_left_to_wait -= sleep_interval
        time.sleep(sleep_interval)

    assert False, f"waited longer than {max_wait} secs for {action}!"


def wait_for_orion(max_wait: float = 10.0, sleep_interval: float = 0.5):
    client = orion_client()

    def can_list_entities():
        try:
            client.list_entities()
            return True
        except BaseException:
            return False

    wait_until(can_list_entities, max_wait, sleep_interval)

