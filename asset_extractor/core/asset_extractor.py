# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '01 Jun 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from asset_extractor.core.handler_pickers import HandlerPicker
from asset_extractor.output_backends.base import OutputBackend
from .util import load_plugins

from typing import Optional, List
import logging

LOGGER = logging.getLogger(__name__)


class AssetExtractor:
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

    def __init__(self, conf: dict):
        self.conf = conf

        # Load entry points
        self.media_handlers = HandlerPicker('media_handlers')

        # Load output backend
        self.output_handlers = load_plugins(conf, 'output_backends', 'outputs')

    def process_file(self, path: str, media: str, checksum: Optional[str] = None) -> None:
        media_handler = self.media_handlers.get_handler(media)

        data = media_handler.get_metadata(path, checksum)

        for backend in self.output_handlers:
            backend.export(data)
