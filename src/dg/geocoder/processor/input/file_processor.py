import logging

from dg.geocoder.config import get_log_config_path
from dg.geocoder.processor.input.base_processor import BaseProcessor
from dg.geocoder.processor.input.document_processor import DocumentProcessor
from dg.geocoder.processor.input.xml_processor import XMLProcessor
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
            if is_xml(self.file):
                return XMLProcessor(self.file, step_logger=self.step_logger).process()
            else:
                return DocumentProcessor(self.file, step_logger=self.step_logger, cty_codes=self.cty_codes).process()
