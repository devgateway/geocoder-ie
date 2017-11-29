import logging.config

from dg.geocoder.config import get_log_config_path
from dg.geocoder.db.activity import get_activity_by_id
from dg.geocoder.iati.activity_reader import ActivityReader

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()


def process_activity(job):
    id = job.get('id')
    activity_id = job.get('activity_id')
    activity = get_activity_by_id(activity_id)

    reader = ActivityReader(xml=activity.get('xml'))

    logger.info("{} {}".format(id, activity_id))
