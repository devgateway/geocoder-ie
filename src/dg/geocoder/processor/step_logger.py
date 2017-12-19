import logging

from dg.geocoder.config import get_log_config_path

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()

# DB processors
from dg.geocoder.constants import ST_PROCESSING
from dg.geocoder.db.doc_queue import update_queue_status


def db_step_logger(queue_id):
    def log(step):
        update_queue_status(queue_id, ST_PROCESSING, message=step)

    return log


def console_step_logger():
    def log(step):
        logger.info('............{}.........'.format(step) )

    return log
