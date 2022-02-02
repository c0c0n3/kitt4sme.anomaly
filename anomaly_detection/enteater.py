"""
Eats NGSI entities for breakfast.

Endpoint to process machine entity updates from Orion.

"""

from anomaly_detection.ai import predict
import anomaly_detection.config as config
import anomaly_detection.log as log
from anomaly_detection.ngsy import MachineEntity, AnomalyDetectionEntity
from anomaly_detection.util.ngsi.headers import FiwareContext
from anomaly_detection.util.ngsi.orion import OrionClient


def process_update(ctx: FiwareContext, ms: [MachineEntity]):
    log.going_to_process_updates(ctx, ms)

    estimates = [predict(m) for m in ms]
    update_context(ctx, estimates)


def update_context(ctx: FiwareContext, estimates: [AnomalyDetectionEntity]):
    log.going_to_update_context_with_estimates(ctx, estimates)

    orion = OrionClient(config.orion_base_url(), ctx)
    orion.upsert_entities(estimates)
