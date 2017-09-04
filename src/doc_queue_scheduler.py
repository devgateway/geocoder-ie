from apscheduler.schedulers.blocking import BlockingScheduler

from dg.geocoder.processor import process_queue

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=30)
def timed_job():
    process_queue()

sched.start()
