import unittest

from dg.geocoder.db.doc_queue import get_queue_list, add_job_to_queue
from dg.geocoder.processor.file_processor import FileProcessor
from dg.geocoder.processor.job_processor import JobProcessor


class TestGeocoder(unittest.TestCase):
    def test_queue(self):
        add_job_to_queue("afdb_subnational.pdf", "application/pdf", "GN", state='ST_TESTING')
        job = get_queue_list(1, 1, ["ST_TESTING"]).get('rows')[0]
        JobProcessor(job).process().save_output()
        processor = FileProcessor('resources/dfid_4182791.odt')
        processor.process()
        processor.get_locations()
        ##self.assertTrue('Dhaka North City Corporation' in [a['name'] for (a, b) in processor.get_locations()])
