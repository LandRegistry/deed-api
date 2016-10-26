import requests
import logging
from application import config


LOGGER = logging.getLogger(__name__)


def perform_check(title):  # pragma: no cover
    resp = requests.get(config.TITLE_ADAPTOR_BASE_HOST + "/titlenumber/" + title)

    LOGGER.info("Making title validator call")

    return resp


def check_health():
    service_response = requests.get(config.TITLE_ADAPTOR_BASE_HOST + '/health/service-check')

    return service_response
