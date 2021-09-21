"""

"""

import os
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path
import logging

import boto3
from botocore.exceptions import ClientError
from asset_extractor.core.base_media_handler import BaseMediaHandler
from asset_scanner.core.utils import generate_id

from typing import Optional

LOGGER = logging.getLogger(__name__)


class ObjectStoreHandler(BaseMediaHandler):
    """
    Extracts metadata from objects held in object store.
    """

    MEDIA_TYPE = 'Object Store'

    def run(self, url, source_media, checksum=None, **kwargs):
        """

        :param path:
        :param source_media:
        :param checksum:
        :param kwargs:
        :return:

        """

        LOGGER.info(f'Extracting metadata for: {url} with checksum: {checksum}')
        
        parse = urlparse(url)
        endpoint_url = f'{parse.scheme}://{parse.netloc}'
        url_path = Path(parse.path)
        bucket = url_path.parts[1]
        path = '/'.join(url_path.parts[2:])

        if 'client' in kwargs:
            s3 = kwargs.get('client')
        else:
            session = boto3.session.Session(**kwargs['session_kwargs'])
            s3 = session.client(
                's3',
                endpoint_url=endpoint_url,
            )
        
        try:
            stats = s3.head_object(
                Bucket=bucket,
                Key=path
            )
        except ClientError:
            stats = {}

        self.info['filepath_type_location'] = path
        self.info['time'] = datetime.now()
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
            self.info[name] = stats.get(attribute)
        except Exception as e:
            LOGGER.debug(e)

    def extract_filename(self, path: str) -> dict:
        try:
            self.info['filename'] = os.path.basename(path)
        except Exception as e:
            LOGGER.debug(e)

    def extract_extension(self, path: str) -> dict:
        try:
            if os.path.splitext(path)[1] != '':
                self.info['extension'] = os.path.splitext(path)[1]
        except Exception as e:
            LOGGER.debug(e)

    def extract_checksum(self, stats: dict, checksum: Optional[str] = None) -> dict:
        # Check if the checksum is the right length for md5 (32 chars)
        if checksum and len(checksum) != 32:
            checksum = None

        if not checksum:
            try:
                checksum =  stats.get('ETag')
            except Exception as e:
                LOGGER.debug(e)
                return

        # Assuming no errors we can now store the checksum
        self.info['checksum'] = checksum
