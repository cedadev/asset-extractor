# encoding: utf-8
"""
Elasticsearch
-------------

An output backend which outputs the content generated to elasticsearch
using the Elasticsearch API

Backend name: ``elasticsearch``

Example Configuration:

    .. code-block:: yaml

        outputs:
            - name: elasticsearch
              connection_kwargs:
                hosts: ['host1','host2']

"""
__author__ = 'Richard Smith'
__date__ = '01 Jun 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from .base import OutputBackend


class ElasticsearchOutputBackend(OutputBackend):
    """
    Connects to an elasticsearch instance and exports the
    documents to elasticsearch.

    """

    def export(self, data, **kwargs):
        print('Exporting to elasticsearch')