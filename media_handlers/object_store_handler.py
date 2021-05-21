import os
import boto3
from core.base_handler import BaseHandler

class ObjectStoreHandler(BaseHandler):
    
    def __init__(self, path, checksum):
        client = boto3.client(service_name='s3', use_ssl=True)
        stats = client.head_object(
            Bucket='bucketname',
            Key=path
        )
        
        self._info = {
            'size': stats.ContentLength,
            'extension': stats.ContentType,
            'mtime': stats.LastModified,
            'magic_number': stats.ContentType,
            'media_type': 'Object Store',
            'filepath_type_location': path,
            'checksum': {
                'time': 'None',
                'checksum': checksum if checksum else stats.ETag,
            }
        }
