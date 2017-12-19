import unittest

from dg.geocoder.db.doc_queue import get_queue_list, add_job_to_queue, delete_all_docs_from_queue
from dg.geocoder.processor.file_processor import FileProcessor
from dg.geocoder.processor.job_processor import JobProcessor


class TestGeocoder(unittest.TestCase):
    def test_queue(self):
        delete_all_docs_from_queue()
        add_job_to_queue("3971744.odt", "application/pdf", "", state='ST_TESTING')
        job = get_queue_list(1, 1, ["ST_TESTING"]).get('rows')[0]
        JobProcessor(job).process().save_output()