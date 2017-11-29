import logging.config

from apscheduler.schedulers.blocking import BlockingScheduler

from dg.geocoder.config import get_doc_queue_path, get_log_config_path
from dg.geocoder.constants import ST_PENDING
from dg.geocoder.db.doc_queue import get_docs
from dg.geocoder.processor.input.job_processor import JobProcessor

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()

# def process_by_id(doc_id):
#    logger.info('Getting doc record')
# doc = get_document_by_id(doc_id)
# process_queue(doc, out_path=get_doc_queue_path())

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=30, max_instances=4)
def timed_job():
    get_jobs()


#sched.start()


# get all pending jobs
def get_jobs():
    pending_jobs = get_docs(1, 10, [ST_PENDING]).get('rows')
    for job in pending_jobs:
        out_path = get_doc_queue_path()
        JobProcessor(job).process()


if __name__ == '__main__':
    get_jobs()
