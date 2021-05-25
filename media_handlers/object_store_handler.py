import os
import hashlib
import boto3
from core.base_handler import BaseHandler

class ObjectStoreHandler(BaseHandler):
    
    MEDIA_TYPE = 'Object Store'

    def __init__(self):
        self.client = boto3.client(service_name='s3', use_ssl=True)
        super().__init__()

    def extract_stat(self, name, stats, attribute):
        try:
             self.info[name] = getattr(stats, attribute)
        except AttributeError:
            pass

    def get_meta_data(self, path, checksum):
        stats = self.client.head_object(
            Bucket='bucketname',
            Key=path
        )

        self.info['filepath_type_location'] = path
        self.extract_id(path)
        self.extract_filename(path)
        self.extract_extension(path)
        self.extract_stat('size', stats, 'ContentLength')
        self.extract_stat('mtime', stats, 'LastModified')
        self.extract_stat('magic_number', stats, 'ContentType')
        self.extract_checksum(stats, checksum)

        return self.info

    def extract_id(self, path):
        try:
            self.info['_id'] = hashlib.md5(path.encode('utf-8')).hexdigest()
        except:
            pass

    def extract_filename(self, path):
        try:
            self.info['filename'] = os.path.basename(path)
        except:
            pass

    def extract_extension(self, path):
        try:
            self.info['extension'] = os.path.splitext(path)[1]
        except:
            pass

    def extract_checksum(self, stats, checksum):
        if checksum:
            return {
                'time':checksum.time,
                'checksum':checksum.checksum,
            }
        else:
            try:
                return {
                    'time':'now',
                    'checksum':getattr(stats, 'ETag'),
                }
            except AttributeError:
                pass
