import logging

from dg.geocoder.processor.document_processor import DocumentProcessor
from dg.geocoder.processor.xml_processor import XMLProcessor

from dg.geocoder.config import get_log_config_path
from dg.geocoder.processor.base_processor import BaseProcessor
from dg.geocoder.util.file_util import is_valid, is_xml

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()


class FileProcessor(BaseProcessor):
    def __init__(self, file, **kwargs):
        BaseProcessor.__init__(self, file, **kwargs)
        self.file = file
        logger.info('processing file {}'.format(self.file))

    def process(self):
        if not is_valid(self.file):
            logger.info('Not valid file provided')
            return None
        else:
            processor = None
            if is_xml(self.file):
                processor = XMLProcessor(self.file, step_logger=self.step_logger)

            else:
                processor = DocumentProcessor(self.file, step_logger=self.step_logger, cty_codes=self.cty_codes)

            processor.process()

        return processor
