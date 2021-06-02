# encoding: utf-8
"""
The output plugins determine what happens at the end of the
extraction process.

You can configure more than one active plugin, if you wanted
to output the content to more than one place.

Output backends are loaded as named entry points.
"""
__author__ = 'Richard Smith'
__date__ = '01 Jun 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from asset_extractor.output_backends.elasticsearch_backend import ElasticsearchOutputBackend
from .standard_out import StdoutOutputBackend