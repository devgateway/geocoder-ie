import unittest

from dg.geocoder.processor.file_processor import FileProcessor

from dg.geocoder.processor.base_processor import FORMAT_TSV, FORMAT_JSON, FORMAT_XML
from dg.geocoder.processor.step_logger import console_step_logger


class TestGeocoder(unittest.TestCase):
    def test_file_to_tsv(self):
        out_file = FileProcessor("resources/dfid_4182791.odt").process().write_output(out_format=FORMAT_TSV)
        self.assertTrue(out_file, 'out.tsv')

    def test_xml_to_xml(self):
        out_file = FileProcessor("resources/afdb_1_no_docs_activities.xml").process().write_output(
            out_format=FORMAT_XML)
        self.assertTrue(out_file, 'out.xml')

    def test_xml_to_tsv(self):
        out_file = FileProcessor("resources/afdb_1_no_docs_activities.xml").process().write_output(
            out_format=FORMAT_TSV)
        self.assertTrue(out_file, 'out.tsv')

    def test_xml_to_json(self):
        out_file = FileProcessor("resources/afdb_1_no_docs_activities.xml").process().write_output(
            out_format=FORMAT_JSON, out_file="test")
        self.assertTrue(out_file, 'test.json')

    def test_afdb_activities_XML(self):
        locations = FileProcessor('resources/afdb_2_activities.xml').process()
        self.assertTrue('' in locations)

    def test_afdb_activities_XML_1(self):
        processor = FileProcessor('resources/afdb_1_no_docs_activities.xml')
        processor.process()
        self.assertTrue('' in processor.get_results())

    def test_dfid_simple_document(self):
        # processor = DocumentProcessor('resources/dfid_4182791.odt', cty_codes=[])
        processor = FileProcessor('resources/dfid_4182791.odt', step_logger=console_step_logger())
        processor.process()
        self.assertTrue(processor.get_locations() is not None)

    def test_xml_simple_doc(self):
        processor = FileProcessor('resources/test_1_activities.xml').process()
        processor.get_locations()
        processor.get_results()

    def test_no_features_in_text(self):
        processor = FileProcessor('resources/no_features_in_text.xml')
        processor.process()
        self.assertTrue('' in processor.get_results())
