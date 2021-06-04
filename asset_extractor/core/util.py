# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '02 Jun 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

# Local imports
from asset_extractor.core.exceptions import NoPluginsError
from asset_extractor.core.handler_pickers import HandlerPicker

# Third party imports
import yaml

# Python imports
import logging
import hashlib

# Typing imports
from typing import List

LOGGER = logging.getLogger(__name__)


def load_plugins(conf: dict, entry_point: str, conf_section: str) -> List:
    """
    Load plugins from the entry points

    :param conf: Configuration dict
    :param entry_point: The name of the collection of entry points
    :param conf_section: The name for the section in the config file
    which applies to these plugins.

    Exceptions:
        NoPluginsError: Triggered if no plugins are successfully loaded

    :return: List of loaded plugins
    """

    loaded_plugins = []

    plugins = HandlerPicker(entry_point)

    for plugin_conf in conf[conf_section]:
        try:
            loaded_plugin = plugins.get_handler(**plugin_conf)
            loaded_plugins.append(loaded_plugin)
        except Exception as e:
            LOGGER.error(f'Failed to load plugin: {plugin_conf["name"]} {e}')

    if not loaded_plugins:
        raise NoPluginsError(f'No plugins were successfully loaded from {conf_section}')

    return loaded_plugins


def generate_id(path):
    return hashlib.md5(path.encode('utf-8')).hexdigest()


def load_yaml(path):
    with open(path) as reader:
        return yaml.load(reader)
