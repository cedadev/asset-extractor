# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '01 Jun 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'


# Framework imports
from asset_scanner.core import BaseExtractor
from asset_scanner.types.source_media import StorageType

# Python imports
from functools import lru_cache
import re
from typing import Optional
import logging



LOGGER = logging.getLogger(__name__)


class AssetExtractor(BaseExtractor):
    """
    The central class for the asset extraction process.

    An instance of the class can be used to atomically process files
    passed to its ``process_file`` method.
    """

    PROCESSOR_ENTRY_POINT = 'asset_extractor.media_handlers'

    @lru_cache(maxsize=3)
    def _load_processor(self, name: StorageType):
        
        name = name.value
        processor_kwargs = self.conf.get(
            'media_handlers', {}
        ).get(
           name, {} 
        )
        
        return self.processors.get_processor(name, **processor_kwargs)

    def process_file(self, filepath: str, source_media: StorageType, checksum: Optional[str] = None, **kwargs) -> None:
        """

        :param filepath:
        :param source_media:
        :param checksum:
        :return:

        """
        processor = self._load_processor(source_media)

        data = processor.run(filepath, source_media, checksum, **kwargs)

        # Get dataset description file
        if self.item_descriptions:

            description_path = self._get_path(filepath, **kwargs)

            description = self.item_descriptions.get_description(description_path)
            categories = self.get_categories(description_path, source_media, description)
            data['body']['categories'] = categories

        self.output(filepath, source_media, data)