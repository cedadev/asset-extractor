# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '01 Jun 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from asset_scanner.core import BaseExtractor
from asset_scanner.core.handler_picker import HandlerPicker

from typing import Optional, List
import logging

LOGGER = logging.getLogger(__name__)


class AssetExtractor(BaseExtractor):
    """
    The central class for the asset extraction process.

    An instance of the class can be used to atomically process files
    passed to its `process_file` method.

    Attributes:
        conf           - Loaded configuration dictionary
        media_handlers - An instance of HandlerPicker which holds reference
                         to the loaded media handlers. Loaded via entry-points
        output_handlers - A list of loaded output handlers, configured using options in
                         the configuration file.
    """

    def load_processors(self):
        return HandlerPicker('asset_extractor.media_handlers')

    def process_file(self, filepath: str, source_media: str, checksum: Optional[str] = None) -> None:
        processor = self.processors.get_handler(source_media)

        data = processor.process(filepath, source_media, checksum)

        for backend in self.output_plugins:
            backend.export(data)
