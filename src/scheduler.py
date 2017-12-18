import logging.config
import os
from apscheduler.schedulers.blocking import BlockingScheduler

from dg.geocoder.config import get_doc_queue_path, get_log_config_path
from dg.geocoder.constants import ST_PENDING
from dg.geocoder.db.doc_queue import get_queue_list, update_queue_out_file
from dg.geocoder.processor.job_processor import JobProcessor

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()

# def process_by_id(doc_id):
#    logger.info('Getting doc record')
# doc = get_queue_by_id(doc_id)
# process_queue(doc, out_path=get_doc_queue_path())

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=10, max_instances=4)
def timed_job():
    process_jobs()


# get all pending jobs
def process_jobs():
    logger.info('process_jobs was called')

    pending_jobs = get_queue_list(1, 10, [ST_PENDING]).get('rows')
    for job in pending_jobs:
        try:
            # TODO: use same db connection across the whole process,connection should be open here and passed to child elements
            processor = JobProcessor(job)
            processor.process()
            processor.save_output()

            if job.get('queue_type') == 'DOC_QUEUE':
                out_file = processor.write_output(out_path=get_doc_queue_path(),
                                                  out_file='{}_{}_out'.format(job.get('id'),os.path.splitext(job.get('file_name'))[0]))
                update_queue_out_file(job.get('id'), out_file)


        except Exception as e:
            logger.error("Job {} did't go well, results were not saved, I THINK ...".format(job.get('id')))
            logger.error(e)


sched.start()
# process_jobs()
