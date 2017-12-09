import unittest

from dg.geocoder.db.doc_queue import get_queue_list, add_job_to_queue
from dg.geocoder.processor.file_processor import FileProcessor
from dg.geocoder.processor.job_processor import JobProcessor


class TestGeocoder(unittest.TestCase):
    def test_queue(self):
        add_job_to_queue("example.xml", "application/xml", "", state='ST_TESTING')
        job = get_queue_list(1, 1, ["ST_TESTING"]).get('rows')[0]
        JobProcessor(job).process().save_output()