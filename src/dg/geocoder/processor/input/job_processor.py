import logging

from dg.geocoder.config import get_log_config_path
from dg.geocoder.constants import ST_PROCESSING, ST_ERROR
from dg.geocoder.db.activity import get_activity_by_id
from dg.geocoder.db.doc_queue import update_doc_status
from dg.geocoder.iati.activity_reader import ActivityReader
from dg.geocoder.processor.input.activity_processor import ActivityProcessor
from dg.geocoder.processor.output.db import persist_geocoding

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()


class JobProcessor:
    def __init__(self, job):
        self.results = []
        self.locations = []
        self.job_queue_type = job.get('queue_type')
        self.job_id = job.get('id')
        self.job_file_name = job.get('file_name')
        self.job_file_type = job.get('file_type')
        self.job_state = job.get('state')
        self.job_create_date = job.get('create_date')
        self.job_processed_date = job.get('processed_date')
        self.job_country_iso = job.get('country_iso')
        self.job_message = job.get('message')
        self.job_activity_id = job.get('activity_id')
        logger.info('processing job {}'.format(self.job_id))

    def process(self):
        try:
            logger.info('processing job {}'.format(self.job_id))
            update_doc_status(self.job_id, ST_PROCESSING, message='Process has been started')

            if self.job_queue_type == 'ACTIVITY_QUEUE':
                activity = get_activity_by_id(self.job_activity_id)
                processor = ActivityProcessor(ActivityReader(xml=activity.get('xml')))
                processor.process()
                self.results = self.results + processor.get_results()
                self.locations = self.locations + processor.get_locations()
                logging.info(len(self.locations))
                persist_geocoding(processor.get_results(), self.job_activity_id, self.job_id, None)
            else:
                pass
        except Exception as error:
            logger.info("Oops!  something didn't go well", error)
            update_doc_status(self.job_id, ST_ERROR, message=error.__str__())
