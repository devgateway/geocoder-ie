import logging

from dg.geocoder.queue_processor.step_logger import step_log

from dg.geocoder.config import get_log_config_path

logging.config.fileConfig(get_log_config_path())
logger = logging.getLogger()


class FileProcessor:
    def __init__(self, file, step_logger=step_log, out_path=None):
        self.file = file
        self.step_logger = step_logger
        self.out_path = out_path
        logger.info('processing file {}'.format(self.file))
