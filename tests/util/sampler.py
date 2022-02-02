import random
import time
from datetime import datetime
from anomaly_detection.ngsy import MachineEntity
from anomaly_detection.util.ngsi.entity import FloatAttr, TextAttr, BooleanAttr
from anomaly_detection.util.ngsi.orion import OrionClient
from tests.util.fiware import orion_client

import string


class MachineSampler:

    def __init__(self, machines_n: int, orion: OrionClient = None):
        self._machines_n = machines_n
        self._orion = orion if orion else orion_client()

    def _ensure_nid_bounds(self, nid: int):
        assert 0 < nid <= self._machines_n

    def generate_rndm(self):
        digit_char = digit_char = random.choices(string.ascii_uppercase, k=2)
        random.shuffle(digit_char)
        return "NAA3U" + ''.join(digit_char)

    def new_machine_entity(self, nid: int) -> MachineEntity:
        self._ensure_nid_bounds(nid)

        seed = random.uniform(0, 1)
        m = MachineEntity(id='',
                          Barcode=TextAttr.new(self.generate_rndm()),
                          Face=TextAttr.new(random.choices(['1st', '2nd'], k=1)[0]),
                          Cell=TextAttr.new(random.choices(list(map(lambda x: str(x), range(1, 113))), k=1)[0]),
                          Point=TextAttr.new(random.choices(['1st', '2nd'], k=1)[0]),
                          Group=TextAttr.new('A+E1'),
                          Joules=FloatAttr.new(random.choices(range(1, 21), k=1)[0] + seed),
                          Charge=FloatAttr.new(random.choices(range(1, 21), k=1)[0] + seed),
                          Residue=FloatAttr.new(random.choices(range(1, 21), k=1)[0] + seed),
                          Force_N=FloatAttr.new(random.choices(range(1, 21), k=1)[0] + seed),
                          Force_N_1=FloatAttr.new(random.choices(range(1, 21), k=1)[0] + seed),
                          Datetime=TextAttr.new(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                          )

        m.set_id_with_type_prefix(f"{nid}")

        return m

    def entity_id(self, nid: int) -> str:
        return self.new_machine_entity(nid).id

    def send_machine_readings(self, nid: int) -> MachineEntity:
        machine = self.new_machine_entity(nid)
        self._orion.upsert_entity(machine)
        return machine

    def sample(self, samples_n: int, sampling_rate: float):
        for _ in range(samples_n):
            ms = [self.new_machine_entity(nid)
                  for nid in range(1, self._machines_n + 1)]
            self._orion.upsert_entities(ms)

            time.sleep(sampling_rate)


# x = MachineSampler(2)
# print(x.new_machine_entity(1))
# print(x.new_machine_entity(2))
# y = x.new_machine_entity(1)
# print(y)
# print(type(y))
# z = x.send_machine_readings(1)
# print(z)
#
# def generate_rndm():
#     digit_char = random.choices(string.ascii_uppercase, k=2)
#     random.shuffle(digit_char)
#     return "NAA3U" + ''.join(digit_char)
# seed = random.uniform(0, 1)
# m = MachineEntity(id='',
#                   Barcode=TextAttr.new(generate_rndm()),
#                   Face=TextAttr.new(random.choices(['1st', '2nd'], k=1)[0]),
#                   Cell=TextAttr.new(random.choices(list(map(lambda x: str(x), range(1, 113))), k=1)[0]),
#                   Point=TextAttr.new(random.choices(['1st', '2nd'], k=1)[0]),
#                   Group=TextAttr.new('A+E1'),
#                   Joules=FloatAttr.new(random.choices(range(1, 21), k=1)[0] + seed),
#                   Charge=FloatAttr.new(random.choices(range(1, 21), k=1)[0] + seed),
#                   Residue=FloatAttr.new(random.choices(range(1, 21), k=1)[0] + seed),
#                   Force_N=FloatAttr.new(random.choices(range(1, 21), k=1)[0] + seed),
#                   Force_N_1=FloatAttr.new(random.choices(range(1, 21), k=1)[0] + seed),
#                   Datetime=TextAttr.new(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#                 )
#
# print(m.json())
