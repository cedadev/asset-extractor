"""
POSIX based metadata extraction
"""

import os
import hashlib
from datetime import datetime
import logging

import magic
from asset_extractor.core.base_handlers import BaseMediaHandler

from typing import Optional


LOGGER = logging.getLogger(__name__)


class PosixHandler(BaseMediaHandler):
    """
    Extracts metadata from POSIX based files
    """

    MEDIA_TYPE = 'POSIX'

    def get_metadata(self, path: str, checksum: Optional[str] = None) -> dict:

        LOGGER.info(f'Extracting metadata for: {path} with checksum: {checksum}')

        stats = os.stat(path)

        self.info['filepath_type_location'] = path
        self.generate_id(path)
        self.extract_filename(path)
        self.extract_extension(path)
        self.extract_stat('size', stats, 'st_size')
        self.extract_stat('mtime', stats, 'st_mtime')
        self.extract_magic_number(path)
        self.extract_checksum(path, checksum)

        return self.info

    def extract_stat(self, name: str, stats: os.stat_result, attribute: str) -> None:
        """
        Trys to retrieve the named attribute

        :param name: Name of the returned stat
        :param stats: Output from os.stat
        :param attribute: The name of the attribute to return
        """
        try:
            self.info[name] = getattr(stats, attribute)
        except AttributeError as e:
            LOGGER.debug(e)

    def extract_filename(self, path: str) -> None:
        try:
            self.info['filename'] = os.path.basename(path)
        except Exceptions as e:
            LOGGER.debug(e)

    def extract_extension(self, path: str) -> None:
        try:
            self.info['extension'] = os.path.splitext(path)[1]
        except Exception as e:
            LOGGER.debug(e)

    def extract_magic_number(self, path: str) -> None:
        try:
            self.info['magic_number'] = magic.from_file(path, mime=True)
        except Exception as e:
            LOGGER.debug(e)

    def extract_checksum(self, path: str, checksum: str) -> None:

        # Check if the checksum is the right length for md5 (32 chars)
        if checksum and len(checksum) != 32:
            checksum = None

        if not checksum:
            try:
                hash_md5 = hashlib.md5()
                with open(path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
            except Exception as e:
                LOGGER.debug(e)
                return

            checksum = hash_md5.hexdigest()

        # Assuming no errors we can now store the checksum
        self.info['checksum'] = {
            'time': datetime.now(),
            'checksum': checksum
        }


