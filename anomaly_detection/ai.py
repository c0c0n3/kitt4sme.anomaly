"""
Predicts whether the datapoint is anomaly or not.
"""
# import sys, os

# scriptdir = os.path.dirname(os.path.realpath(__file__))

# sys.path.append(os.path.join(scriptdir, 'anomaly_detection'))

# also change cwd to where the script is located (helps for finding relative files)
# print('============\ncwd is %s' %(os.getcwd()))

# os.chdir(scriptdir)
# print('============\ncwd after change to script dir is %s' %(os.getcwd()))

import numpy as np
import pickle

from anomaly_detection.ngsy import BooleanAttr, FloatAttr
from anomaly_detection.ngsy import RawReading, MachineEntity, AnomalyDetectionEntity

ANOMALY_MODEL_PATH_FROM_ROOT = 'data/anomaly_detection.pkl'


with open(ANOMALY_MODEL_PATH_FROM_ROOT, 'rb') as open_file:
    model = pickle.load(open_file)


def predict(machine: MachineEntity) -> AnomalyDetectionEntity:
    label = predict_anomaly(machine)
    #print(label)

    return AnomalyDetectionEntity(id=machine.id,
                                   Label=FloatAttr.new(label))



def predict_anomaly(machine: MachineEntity) -> bool:
    
    global model
    
    x = machine.Joules.value

    return model.predict(np.array(x).reshape(-1,1))[0]
    


# sensors_data = {"Barcode":"ZLM001", "Face": "2nd", "Cell":"8th", "Point":"1st", "Group": "A+E1",
#                 "Joules": 10, "Charge": 100.5, "Residue": 98.24, "Force_N": 24.2,
#                 "Force_N_1": 23.5, "Datetime": "2020-06-08 00:00:00"}
# rr = RawReading(**sensors_data)
# machine1 = MachineEntity(id='').set_id_with_type_prefix('1')
#
# x = rr.to_machine_entity(entity_id=machine1.id)
# print(x.json())
# print(predict(x))
