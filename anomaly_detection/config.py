import os
from uri import URI


ORION_BASE_URL_VAR = 'ORION_BASE_URL'


def orion_base_url() -> URI:
    value = os.environ[ORION_BASE_URL_VAR]
    return URI(value)

# TODO. Robust implementation. See e.g. env readers from QL.