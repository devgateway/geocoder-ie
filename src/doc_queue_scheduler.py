from apscheduler.schedulers.blocking import BlockingScheduler

from dg.geocoder.processor import process_queue

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=30, max_instances=4)
def timed_job():
    process_queue()


sched.start()
