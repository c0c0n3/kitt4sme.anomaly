from anomaly_detection.ngsy import *


def test_float_attr_serialisation():
    want = '{"type": "Number", "value": 2.3}'
    got = FloatAttr.new(2.3).json()
    assert want == got


def test_readings_to_machine_entity_json():
    sensors_data = {"Barcode":"ZLM001", "Face": "2nd", "Cell":"8th", "Point":"1st", "Group": "A+E1",
                "Joules": 4.5, "Charge": 100.5, "Residue": 98.24, "Force_N": 24.2,
                "Force_N_1": 23.5, "Datetime": "2020-06-08 00:00:00"}
    rr = RawReading(**sensors_data)

    machine1 = MachineEntity(id='').set_id_with_type_prefix('1')
    got = rr.to_machine_entity(entity_id=machine1.id).to_json()

    want = '{"id": "urn:ngsi-ld:Machine:1", "type": "Machine", "Barcode": {"type": "Text", "value": "ZLM001"}, "Face": {"type": "Text", "value": "2nd"}, "Cell": {"type": "Text", "value": "8th"}, "Point": {"type": "Text", "value": "1st"}, "Group": {"type": "Text", "value": "A+E1"}, "Joules": {"type": "Number", "value": 4.5}, "Charge": {"type": "Number", "value": 100.5}, "Residue": {"type": "Number", "value": 98.24}, "Force_N": {"type": "Number", "value": 24.2}, "Force_N_1": {"type": "Number", "value": 23.5}, "Datetime": {"type": "Text", "value": "2020-06-08 00:00:00"}}'
    assert want == got
