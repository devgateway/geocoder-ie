import logging
import os

from dg.geocoder.config import get_log_config_path, get_doc_queue_path
from dg.geocoder.constants import ST_PROCESSING, ST_ERROR, ST_PROCESSED
from dg.geocoder.db.activity import get_activity_by_id
from dg.geocoder.db.db import close, open
from dg.geocoder.db.doc_queue import update_queue_status
from dg.geocoder.db.geocode import save_geocoding, save_extract_text
from dg.geocoder.iati.activity_reader import ActivityReader
from dg.geocoder.processor.activity_processor import ActivityProcessor
from dg.geocoder.processor.base_processor import BaseProcessor
from dg.geocoder.processor.file_processor import FileProcessor
from dg.geocoder.processor.step_logger import db_step_logger

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()


class JobProcessor(BaseProcessor):
    def __init__(self, job, **kwargs):
        BaseProcessor.__init__(self, job, **kwargs)
        self.results = []
        self.processor = None
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
        self.step_logger = db_step_logger(job.get('id'))

        logger.info('processing job {}'.format(self.job_id))

    def process(self):
        try:
            logger.info('processing job {}'.format(self.job_id))
            update_queue_status(self.job_id, ST_PROCESSING, message='Process has been started')

            if self.job_queue_type == 'ACTIVITY_QUEUE':
                activity = get_activity_by_id(self.job_activity_id)
                self.processor = ActivityProcessor(ActivityReader(xml=activity.get('xml')),
                                                   step_logger=self.step_logger)
                self.processor.process()
                self.results = self.results + self.processor.get_results()
                self.locations = self.locations + self.processor.get_locations()
            else:
                self.processor = FileProcessor(os.path.join(get_doc_queue_path(), self.job_file_name),
                                               cty_codes=[self.job_country_iso], step_logger=self.step_logger)
                self.processor.process()
                self.results = self.results + self.processor.get_results()
                self.locations = self.locations + self.processor.get_locations()
                return self

        except Exception as error:
            logger.info("Oops!  something didn't go well", error)
            update_queue_status(self.job_id, ST_ERROR, message=error.__str__())
            raise

    def save_output(self):
        try:
            self.persist_geocoding(self.get_results(), self.job_activity_id, self.job_id)
            update_queue_status(self.job_id, ST_PROCESSED)
            return self
        except Exception as error:
            logger.error(error)
            update_queue_status(self.job_id, ST_ERROR, message=error.__str__())

    def persist_geocoding(self, results, activity_id, job_id):
        geocoding_list = [(data['geocoding'], data['texts']) for (l, data) in results if data.get('geocoding')]
        for geocoding in geocoding_list:
            try:
                conn = open()
                location_id, geocoding_id = save_geocoding(geocoding[0], job_id, activity_id, conn=conn)
                for text in geocoding[1]:
                    save_extract_text(text.get('text'), geocoding_id, location_id, job_id,
                                      ', '.join(text.get('entities')),
                                      conn=conn)

                conn.commit()
            except Exception as error:
                conn.cancel()
                logger.info(error)
                raise
            finally:
                close(conn)
        return None
