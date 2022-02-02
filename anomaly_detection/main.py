from fastapi import FastAPI, Header, Request
from typing import Optional

from anomaly_detection.enteater import process_update
import anomaly_detection.log as log
from anomaly_detection.ngsy import MachineEntity, RawReading
from anomaly_detection.util.ngsi.entity import EntityUpdateNotification
from anomaly_detection.util.ngsi.headers import FiwareContext
from anomaly_detection.ai import predict

import uvicorn, json

VERSION = '0.1.0'

app = FastAPI()


@app.get('/')
def read_root():
    return {'AnomalyDetector': VERSION}


@app.get("/version")
def read_version():
    return read_root()


@app.post("/updates")
def post_updates(notification: EntityUpdateNotification,
                 fiware_service: Optional[str] = Header(None),
                 fiware_servicepath: Optional[str] = Header(None),
                 fiware_correlator: Optional[str] = Header(None)):
    ctx = FiwareContext(
        service=str(fiware_service), service_path=str(fiware_servicepath),
        correlator=str(fiware_correlator)
    )

    log.received_ngsi_entity_update(ctx, notification)

    updated_machines = notification.filter_entities(MachineEntity)
    if updated_machines:
        process_update(ctx, updated_machines)



@app.post("/rawReading")
async  def raw_reading(data: Request):
    req_info = await data.json()
    #print(req_info)
    if req_info.get('id', 0):
        machine1 = MachineEntity(id='').set_id_with_type_prefix(req_info.get('id'))
        req_info.pop('id')
    else:
        machine1 = MachineEntity(id='').set_id_with_type_prefix('1')
    rr = RawReading(**req_info)

    x = rr.to_machine_entity(entity_id=machine1.id)

    out = json.loads(predict(x).to_json())


    return {"Label": out['Label']['value']}


# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=8001)