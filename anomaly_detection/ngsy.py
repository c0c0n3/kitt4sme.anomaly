"""
Roughnator NGSI v2 data types.

Examples
--------

>>> from anomaly_detection.util.ngsi.entity import *
>>> from anomaly_detection.ngsy import *


1. NGSI attributes from values.

>>> FloatAttr.new(2.3).json()
'{"type": "Number", "value": 2.3}'
>>> print(TextAttr.new('hi'))
type='Text' value='hi'


2. NGSI entity from JSON---ignores unknown attributes.

>>> BaseEntity.parse_raw('{"id": "1", "type": "foo", "x": 3}')
BaseEntity(id='1', type='foo')


3. Build entity with preformatted ID

>>> machine1 = MachineEntity(id='').set_id_with_type_prefix('1')
>>> machine1.id, machine1.type
('urn:ngsi-ld:Machine:1', 'Machine')


4. Don't serialise unset NGSI attributes.

>>> machine1.to_json()
'{"id": "urn:ngsi-ld:Machine:1", "type": "Machine"}'


5. Build sensors data from dictionary.

>>> sensors_data = {"BarCode":"ZLM001", "Face": "2nd", "Cell":"8th", "Point":"1st", "Group": "A+E1", 
                    "Output Joules": 17.55, "Charge (v)": 100.5, "Residue (v)": 98.24, "Force L N": 24.2, 
                    "Force L N_1": 23.5, "Y/M/D hh:mm:ss": "2020-06-08 00:00:00"}
>>> rr = RawReading(**sensors_data)
>>> print(rr)
Output Joules= 17.55 Charge (v)= 100.5 Residue (v)= 98.24 Force L N= 24.2 Force L N_1​= 23.5


6. Transform sensors data to machine entity and serialise it.

>>> rr.to_machine_entity(entity_id=machine1.id).to_json()
'{"id": "urn:ngsi-ld:Machine:1", "type": "Machine", \
"BarCode": {"type": "Text", "value": "ZLM001"}, \
"Face": {"type": "Text", "value": "2nd"}, \
"Cell": {"type": "Text", "value": "8th", \
"Point": {"type": "Text", "value": "1st"}, \
"Group": {"type": "Text", "value": "A+E1"}, \
"Output Joules": {"type": "Number", "value": 17.55}, \
"Charge (V)": {"type": "Number", "value": 100.5}, \
"Residue (V)": {"type": "Number", "value": 98.24,}, \
"Force L N": {"type": "Number", "value": 24.2}, \
"Force L N_1​": {"type": "Number", "value": 23.5}, \
"Y/M/D hh:mm:ss": {"type": "Text", "value": "2020-06-08 00:00:00"}}'


7. Same as (6) but now some readings are missing.

>>> rr = RawReading(Output Joules= 17.55 Charge (v)= 100.5 Residue (v)= 98.24 Force L N= 24.2 Force L N_1​= 23.5)
>>> rr.to_machine_entity(entity_id=machine1.id).to_json()
'{"id": "urn:ngsi-ld:Machine:1", "type": "Machine", \
"Output Joules": {"type": "Number", "value": 17.55}, \
"Charge (V)": {"type": "Number", "value": 100.5}, \
"Residue (V)": {"type": "Number", "value": 98.24,}, \
"Force L N": {"type": "Number", "value": 24.2}, \
"Force L N_1​": {"type": "Number", "value": 23.5}}'


8. Build Anomaly detector and serialise it.

>>> ai = AnomalyDetectionEntity(id=machine1.id,
...                              output_joules=FloatAttr.new(2.3))
>>> ai.json()
'{"id": "urn:ngsi-ld:Machine:1", "type": "AnomalyDetector", \
"output_joules": {"type": "Number", "value": 2.3}}'


9. Filter machine entities out of an NGSI update notification.

>>> notification = EntityUpdateNotification(
...    data=[
...        {"id": "1", "type": "Machine", "Ra": {"value": 1.1}},
...        {"id": "2", "type": "NotMe", "Ra": {"value": 2.2}},
...        {"id": "3", "type": "Machine", "Ra": {"value": 3.3}}
...    ]
... )
>>> notification.filter_entities(MachineEntity)
[MachineEntity(id='1', type='Machine', AcelR=None, fz=None, Diam=None, \
ae=None, HB=None, geom=None, Ra=FloatAttr(type='Number', value=1.1)), \
MachineEntity(id='3', type='Machine', AcelR=None, fz=None, Diam=None, \
ae=None, HB=None, geom=None, Ra=FloatAttr(type='Number', value=3.3))]

"""

from email.headerregistry import Group
from pydantic import BaseModel
from typing import Optional

from anomaly_detection.util.ngsi.entity import BaseEntity, FloatAttr, TextAttr, BooleanAttr, EntityUpdateNotification


class MachineEntity(BaseEntity):
    type = 'Machine'
    
    Barcode: Optional[TextAttr]
    Face: Optional[TextAttr]
    Cell: Optional[TextAttr]
    Point: Optional[TextAttr]
    Group: Optional[TextAttr]
    
    Joules: Optional[FloatAttr]
    Charge: Optional[FloatAttr]
    Residue: Optional[FloatAttr]
    Force_N: Optional[FloatAttr]
    Force_N_1: Optional[FloatAttr]
    
    Datetime: Optional[TextAttr]


class RawReading(BaseModel):
    Barcode: Optional[str]
    Face: Optional[str]
    Cell: Optional[str]
    Point: Optional[str]
    Group: Optional[str]
    Joules: Optional[float]
    Charge: Optional[float]
    Residue: Optional[float]
    Force_N: Optional[float]
    Force_N_1: Optional[float]
    Datetime: Optional[str]

    def to_machine_entity(self, entity_id) -> MachineEntity:
        e = MachineEntity(id=entity_id)
        
        e.Barcode = TextAttr.new(self.Barcode)
        e.Face = TextAttr.new(self.Face)
        e.Cell = TextAttr.new(self.Cell)
        e.Point = TextAttr.new(self.Point)
        e.Group = TextAttr.new(self.Group)
        e.Joules = FloatAttr.new(self.Joules)
        e.Charge = FloatAttr.new(self.Charge)
        e.Residue = FloatAttr.new(self.Residue)
        e.Force_N = FloatAttr.new(self.Force_N)
        e.Force_N_1 = FloatAttr.new(self.Force_N_1)
        e.Datetime = TextAttr.new(self.Datetime)

        return e
    
class AnomalyDetectionEntity(BaseEntity):
    type = 'AnomalyDetection'
    #sensor = dict
    Label: FloatAttr



# print(FloatAttr.new(2.3.json()))
# print(TextAttr.new('hi').json())

# foo = BaseEntity.parse_raw('{"id": "1", "type": "foo", "x": 3}')
# print(foo)

# machine1 = MachineEntity(id='').set_id_with_type_prefix('1')
# # print(machine1)
# print(machine1.to_json())
#
# sensors_data = {"Barcode":"ZLM001", "Face": "2nd", "Cell":"8th", "Point":"1st", "Group": "A+E1",
#                 "Joules": 4.5, "Charge": 100.5, "Residue": 98.24, "Force_N": 24.2,
#                 "Force_N_1": 23.5, "Datetime": "2020-06-08 00:00:00"}
# rr = RawReading(**sensors_data)
# # print(rr)
# # print(rr.to_machine_entity(entity_id=machine1.id).to_json())
#
# rr = RawReading(Joules=10)
# # print(rr)
# # print(rr.to_machine_entity(entity_id=machine1.id).to_json())
# x = rr.to_machine_entity(entity_id=machine1.id)
# ai = AnomalyDetectionEntity(
#     id=machine1.id,
#     Label=BooleanAttr.new(1))
# print(ai.json())

# notification = EntityUpdateNotification(
#     data=[
#         {"id": "1", "type": "Machine", "Joules": {"value": 1.1}},
#         {"id": "2", "type": "NotMe", "Joules": {"value": 2.2}},
#         {"id": "3", "type": "Machine", "Joules": {"value": 3.3}}
#     ]
# )
# print(notification.filter_entities(MachineEntity))

