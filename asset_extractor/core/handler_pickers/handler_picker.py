# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '01 Jun 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import pkg_resources
from asset_extractor.core.base_handlers import BaseHandler


class HandlerPicker:
    def __init__(self, entry_point_key: str):
        """
        Entry points to load from in the setup.py

        :param entry_point_key: name of the entry point source
        """
        self.handlers = {}
        for entry_point in pkg_resources.iter_entry_points(entry_point_key):
            self.handlers[entry_point.name] = entry_point.load()

    def get_handler(self, name: str, **kwargs) -> BaseHandler:
        """
        Get the handler by name

        :param name: The name of the required handler

        :return: An instance of the requested handler
        """
        return self.handlers[name](**kwargs)
