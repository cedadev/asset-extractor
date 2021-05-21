
from abc import ABC, abstractmethod

class BaseHandler(ABC):
    
    @abstractmethod
    def __init__(self, path, checksum):
        """
        Constructor for self._info.
        """
        self._info = {
            'size': 'int',
            'extension': 'string',
            'mtime': 'date',
            'magic_number': 'string',
            'media_type': 'string',
            'filepath_type_location': 'string',
            'checksum': {
                'time': 'date',
                'checksum': checksum if checksum else 'string',
            }
        }
    
    @property
    def info(self):
        return self._info
