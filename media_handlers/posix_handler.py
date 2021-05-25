import os
import hashlib
from datetime import datetime

import magic
from core.base_handler import BaseHandler

class PosixHandler(BaseHandler):

    MEDIA_TYPE = 'POSIX'
    
    def extract_stat(self, name, stats, attribute):
        try:
             self.info[name] = getattr(stats, attribute)
        except AttributeError:
            pass

    def get_meta_data(self, path, checksum):
        stats = os.stat(path)

        self.info['filepath_type_location'] = path
        self.extract_id(path)
        self.extract_filename(path)
        self.extract_extension(path)
        self.extract_stat('size', stats, 'st_size')
        self.extract_stat('mtime', stats, 'st_mtime')
        self.extract_magic_number(path)
        self.extract_checksum(path, checksum)

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

    def extract_magic_number(self, path):
        try:
            self.info['magic_number'] = magic.from_file(path, mime=True)
        except:
            pass

    def extract_checksum(self, path, checksum):
        if checksum:
            self.info['checksum'] = {
                'time':checksum.time,
                'checksum':checksum.checksum,
            }
        else:
            try:
                hash_md5 = hashlib.md5()
                with open(path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)

                self.info['checksum'] = {
                    'time':datetime.now(),
                    'checksum':hash_md5.hexdigest(),
                }
            except AttributeError:
                pass
