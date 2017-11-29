# DB processors
from dg.geocoder.constants import ST_PROCESSING
from dg.geocoder.db.doc_queue import update_doc_status


def step_log(doc_id):
    def log(step):
        update_doc_status(doc_id, ST_PROCESSING, message=step)

    return log
