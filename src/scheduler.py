import logging.config
import os
from apscheduler.schedulers.blocking import BlockingScheduler

from banner import print_banner
from dg.geocoder.config import get_doc_queue_path, get_log_config_path
from dg.geocoder.constants import ST_PENDING
from dg.geocoder.db.doc_queue import get_queue_list, update_queue_out_file, get_pending_queue_list
from dg.geocoder.processor.job_processor import JobProcessor

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()

# def process_by_id(doc_id):
#    logger.info('Getting doc record')
# doc = get_queue_by_id(doc_id)
# process_queue(doc, out_path=get_doc_queue_path())
from datetime import datetime


# get all pending jobs
def process_jobs():
    logger.info('process_jobs was called')
    pending_jobs = get_queue_list(1, 1, [ST_PENDING]).get('rows')
    for job in pending_jobs:
        try:
            # TODO: use same db connection across the whole process,connection should be open here and passed to child elements
            processor = JobProcessor(job)
            processor.process()
            processor.save_output()

            if job.get('queue_type') == 'DOC_QUEUE':
                out_file = processor.write_output(out_path=get_doc_queue_path(),
                                                  out_file='{}_{}_out'.format(job.get('id'),
                                                                              os.path.splitext(job.get('file_name'))[
                                                                                  0]))
                update_queue_out_file(job.get('id'), out_file)


        except Exception as e:
            logger.error("Job {} did't go well, results were not saved, I THINK ...".format(job.get('id')))
            logger.error(e)


# process all pending jobs
def process_all_pending_jobs():
    logger.info('process_all_pending_jobs was called')
    pending_jobs = get_pending_queue_list().get('rows')
    for job in pending_jobs:
        try:
            processor = JobProcessor(job)
            processor.process()
            processor.save_output()
            processor.clean()

        except Exception as e:
            logger.error("Job {} did't go well, results were not saved".format(job.get('id')))
            logger.error(e)


if __name__ == '__main__':
    print_banner()
    scheduler = BlockingScheduler()
    scheduler.add_job(process_jobs, 'interval', seconds=30)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
