# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '01 Jun 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from asset_scanner.core.processor import BaseProcessor
from abc import ABC, abstractmethod
import hashlib

from typing import Optional


class BaseMediaHandler(BaseProcessor):
    """
    Defines the interface for other asset extraction handlers.

    Attributes:
        info -  A dictionary which will hold all the extracted metadata and is
                returned by get_metadata.

    All subclasses must implement the get_metadata method.
    """

    MEDIA_TYPE = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.info = {
            'media_type': self.MEDIA_TYPE,
        }

    @abstractmethod
    def run(self, filepath: str, source_media: str, checksum: Optional[str] = None, **kwargs) -> dict:
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

        :return: The extracted metadata with the format:
        .. code-block:: json

            {
                "id": "generated_ID",
                "body": {}
            }

        where the body is the extracted metadata.
        """

        pass
