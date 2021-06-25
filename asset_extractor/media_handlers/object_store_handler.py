"""

"""

import os
from datetime import datetime

import boto3
from asset_extractor.core.base_media_handler import BaseMediaHandler
from asset_scanner.core.utils import generate_id

from typing import Optional

LOGGER = logging.getLogger(__name__)


class ObjectStoreHandler(BaseMediaHandler):
    """
    Extracts metadata from objects held in object store.
    """

    MEDIA_TYPE = 'Object Store'

    def __init__(self):
        self.client = boto3.client(service_name='s3', use_ssl=True)
        super().__init__()

    def run(self, path, source_media, checksum=None, **kwargs):
        """

        :param path:
        :param source_media:
        :param checksum:
        :param kwargs:
        :return:

        """

        LOGGER.info(f'Extracting metadata for: {path} with checksum: {checksum}')

        stats = self.client.head_object(
            Bucket='bucketname',
            Key=path
        )

        self.info['filepath_type_location'] = path
        self.extract_filename(path)
        self.extract_extension(path)
        self.extract_stat('size', stats, 'ContentLength')
        self.extract_stat('mtime', stats, 'LastModified')
        self.extract_stat('magic_number', stats, 'ContentType')
        self.extract_checksum(stats, checksum)

        return {'id': generate_id(path), 'body': self.info}

    def extract_stat(self, name: str, stats: dict, attribute: str):
        """
        Trys to retrieve the named attribute

        :param name: Name of the returned stat
        :param stats: Output from self.client.head_object
        :param attribute: The name of the attribute to return
        """
        try:
            self.info[name] = getattr(stats, attribute)
        except Exception as e:
            LOGGER.debug(e)

    def extract_filename(self, path: str) -> dict:
        try:
            self.info['filename'] = os.path.basename(path)
        except Exception as e:
            LOGGER.debug(e)

    def extract_extension(self, path: str) -> dict:
        try:
            self.info['extension'] = os.path.splitext(path)[1]
        except Exception as e:
            LOGGER.debug(e)

    def extract_checksum(self, stats: dict, checksum: Optional[str] = None) -> dict:
        # Check if the checksum is the right length for md5 (32 chars)
        if checksum and len(checksum) != 32:
            checksum = None

        if not checksum:
            try:
                checksum =  getattr(stats, 'ETag'),
            except Exception as e:
                LOGGER.debug(e)
                return

        # Assuming no errors we can now store the checksum
        self.info['checksum'] = [
            {
                'time': datetime.now(),
                'checksum': checksum
            }
        ]
