# encoding: utf-8
"""
Simple script to serve as an example.


USAGE:

    usage: extract_assets [-h] [-s {posix,objectstore}] URI

    Simple script to work as an example for the asset extractor

    positional arguments:
      conf                  Path to a configuration file to set the input and
                            output plugin to use.

    optional arguments:
      -h, --help            show this help message and exit

"""
__author__ = 'Richard Smith'
__date__ = '01 Jun 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import argparse
import os
import yaml

from asset_extractor.core.handler_pickers import HandlerPicker
from asset_extractor.core import AssetExtractor
from asset_extractor.core.util import load_plugins


def command_args():
    """
    Sets the command line arguments and handles their parsing
    :return: command line options
    """
    parser = argparse.ArgumentParser(description='Simple script to work run the asset extractor as configured')
    parser.add_argument('conf', help='Path to a yaml configuration file')
    args = parser.parse_args()

    return args


def load_config(path):
    with open(path) as reader:
        conf = yaml.load(reader)
    return conf


def main():
    args = command_args()

    conf = load_config(args.conf)

    extractor = AssetExtractor(conf)

    input_plugins = load_plugins(conf, 'input_plugins', 'inputs')

    for input in input_plugins:
        input.run(extractor)


if __name__ == '__main__':
    main()
