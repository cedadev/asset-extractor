# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '01 Jun 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from abc import ABC, abstractmethod
import hashlib

from typing import Optional

from .base import BaseHandler


class BaseMediaHandler(BaseHandler):
    """
    Defines the interface for other asset extraction handlers.

    Attributes:
        info -  A dictionary which will hold all the extracted metadata and is
                returned by get_metadata.

    All subclasses must implement the get_metadata method.
    """

    MEDIA_TYPE = None

    def __init__(self):
        self.info = {
            'media_type': self.MEDIA_TYPE,
        }

    def generate_id(self, path):
        self.info['_id'] = hashlib.md5(path.encode('utf-8')).hexdigest()

    @abstractmethod
    def get_metadata(self, path: str, checksum: Optional[str] = None) -> dict:
        """
        The entry point for the subclasses. This
        takes the path and an optional checksum
        and extracts as much file-level metadata as it can.

        Subclassed methods should be error hardened so that errors
        when extracting parts of the metadata do not throw
        away other data extracted successfully.

        :param path: The path to analyse
        :param checksum: If a checksum is provided here, it will not be calculated.
        This saves compute.

        :return: The extracted metadata
        """
        pass
