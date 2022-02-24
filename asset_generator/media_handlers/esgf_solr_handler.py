from typing import Optional
from asset_generator.core.base_media_handler import BaseMediaHandler
from asset_scanner.core.utils import generate_id
from asset_scanner.types.source_media import StorageType

import requests
import logging

LOGGER = logging.getLogger(__name__)


class ESGFSolrHandler(BaseMediaHandler):

    MEDIA_TYPE = StorageType.ESGF_SOLR

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        session_kwargs = getattr(self, 'solr_kwargs')
        self.index = session_kwargs.get('index_node')
        self.core = session_kwargs.get('solr_core', 'files')

    def get_file(self, path):
        url = f"http://{self.index}/solr/{self.core}/select"
        search_params = {
            'indent': 'on',
            'q': f'id:{path}',
            'wt': 'json',
            'rows': 1,
            'sort': 'id asc',
            'cursorMark': '*'
        }

        resp = requests.get(url, search_params).json()
        docs = resp["response"]["docs"]
        for doc in docs:
            files = list(doc.items())
            for file in files:
                return file

    def extract_size(self, file: dict):
        self.info['size'] = file['size']

    def extract_checksum(self, file: dict, checksum: str):
        ...

    def extract_extension(self, path: str):
        file_extension = path.split('.')[-1]
        self.info['extension'] = file_extension

    def run(self,
            path,
            source_media: StorageType = StorageType.ESGF_SOLR,
            checksum: Optional[str] = None,
            **kwargs) -> dict:

        file = self.get_file(path)
        self.info = {}

        self.info['location'] = path

        return {'id': generate_id(path), 'body': self.info}
