import logging.config

from apscheduler.schedulers.blocking import BlockingScheduler

from dg.geocoder.config import get_doc_queue_path, get_log_config_path
from dg.geocoder.constants import ST_PENDING
from dg.geocoder.db.doc_queue import get_queue_list
from dg.geocoder.processor.job_processor import JobProcessor

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()

# def process_by_id(doc_id):
#    logger.info('Getting doc record')
# doc = get_queue_by_id(doc_id)
# process_queue(doc, out_path=get_doc_queue_path())

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=30, max_instances=4)
def timed_job():
    process_jobs()


# get all pending jobs
def process_jobs():
    pending_jobs = get_queue_list(1, 10, [ST_PENDING]).get('rows')
    for job in pending_jobs:
        try:
            out_path = get_doc_queue_path()
            JobProcessor(job).process().save_output()
        except:
            logger.error("Job {} did't go well, results were not saved, I THINK ...".format(job.get('id')))



sched.start()
