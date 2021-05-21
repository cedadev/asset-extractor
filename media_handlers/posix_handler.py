import os
import hashlib
import magic
from core.base_handler import BaseHandler

class PosixHandler(BaseHandler):
    
    def __init__(self, path, checksum):
        stats = os.stat(path)
        
        self._info = {
            '_id': 'shahash of path',
            'filename': os.path.basename(path),
            'size': stats.st_size,
            'extension': os.path.splitext(path)[1],
            'mtime': stats.st_mtime,
            'magic_number': magic.from_file(path, mime=True),
            'media_type': 'POSIX',
            'filepath_type_location': path,
            'checksum': {
                'time': 'None',
                'checksum': checksum if checksum else self.md5(path),
            }
        }

    def md5(self, filename):
        hash_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
