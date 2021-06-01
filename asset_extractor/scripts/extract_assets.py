# encoding: utf-8
"""
Simple script to serve as an example.


USAGE:

    usage: extract_assets [-h] [-s {posix,objectstore}] URI

    Simple script to work as an example for the asset extractor

    positional arguments:
      URI                   Path to the files to scan. This could be a POSIX
                            location or a URL to object store

    optional arguments:
      -h, --help            show this help message and exit
      -s {posix,objectstore}, --source {posix,objectstore}
                            The source media type.

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


def command_args():
    """
    Sets the command line arguments and handles their parsing
    :return: command line options
    """
    parser = argparse.ArgumentParser(description='Simple script to work as an example for the asset extractor')

    parser.add_argument('URI',
                        help='Path to the files to scan. This could be a POSIX location or a URL to object store')
    parser.add_argument('conf', help='Path to a yaml configuration file')

    args = parser.parse_args()

    return args


def load_config(path):
    conf = {}

    with open(path) as reader:
        conf = yaml.load(reader)
    return conf

def main():
    args = command_args()

    conf = load_config(args.conf)

    extractor = AssetExtractor(conf)

    for root, _, files in os.walk(args.URI):
        for file in files:
            filename = os.path.abspath(os.path.join(root, file))
            extractor.process_file(filename, 'posix')


if __name__ == '__main__':
    main()
