"""
"""

import os
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path
import logging

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from botocore import UNSIGNED
from asset_extractor.core.base_media_handler import BaseMediaHandler
from asset_scanner.core.utils import generate_id
from asset_scanner.types.source_media import StorageType

from typing import Optional

LOGGER = logging.getLogger(__name__)


class ObjectStoreHandler(BaseMediaHandler):
    """
    Extracts metadata from objects held in object store.

    Configuration options:

    .. list-table::
        :header-rows: 1

        * - Option
          - Value Type
          - Description
        * - ``session_kwargs``
          - ``dict``
          - Parameters passed to `boto3.session.Session <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session>`_

    """

    MEDIA_TYPE = StorageType.OBJECT_STORE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        session_kwargs = getattr(self, 'boto_session_kwargs', {})
        self.session = boto3.session.Session(**session_kwargs)
        self.anonymous = not session_kwargs

    def run(self,
            path,
            source_media: StorageType = StorageType.OBJECT_STORE,
            checksum: Optional[str] = None,
            **kwargs) -> dict:
        """

        :param path:
        :param source_media:
        :param checksum:
        :param kwargs:
        :return:

        """

        LOGGER.info(f'Extracting metadata for: {path} with checksum: {checksum}')

        uri_parse = kwargs.get('uri_parse')
        if not uri_parse:
            uri_parse = urlparse(path)
        
        endpoint_url = f'{uri_parse.scheme}://{uri_parse.netloc}'
        url_path = Path(uri_parse.path)
        bucket = url_path.parts[1]
        object_path = '/'.join(url_path.parts[2:])

        client_kwargs = {}
        if self.anonymous:
            client_kwargs['config'] = Config(signature_version=UNSIGNED)

        s3 = self.session.client(
            's3',
            endpoint_url=endpoint_url,
            **client_kwargs
        )

        try:
            stats = s3.head_object(
                Bucket=bucket,
                Key=path
            )
        except ClientError:
            stats = {}

        self.info['location'] = path
        self.extract_filename(object_path)
        self.extract_extension(object_path)
        self.extract_stat('size', stats, 'ContentLength')
        self.extract_stat('mtime', stats, 'LastModified')
        self.extract_stat('magic_number', stats, 'ContentType')
        self.extract_checksum(stats, checksum)

        return {'id': generate_id(path), 'body': self.info}

    def extract_stat(self, name: str, stats: dict, attribute: str) -> None:
        """
        Trys to retrieve the named attribute

        :param name: Name of the returned stat
        :param stats: Output from self.client.head_object
        :param attribute: The name of the attribute to return
        """
        try:
            value = stats.get(attribute)
            if value:
                self.info[name] = value
        except Exception as e:
            LOGGER.debug(e)

    def extract_filename(self, path: str) -> None:
        try:
            self.info['filename'] = os.path.basename(path)
        except Exception as e:
            LOGGER.debug(e)

    def extract_extension(self, path: str) -> None:
        try:
            if os.path.splitext(path)[1] != '':
                self.info['extension'] = os.path.splitext(path)[1]
        except Exception as e:
            LOGGER.debug(e)

    def extract_checksum(self, stats: dict, checksum: Optional[str] = None) -> None:
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
        if checksum:
            self.info['checksum'] = checksum
