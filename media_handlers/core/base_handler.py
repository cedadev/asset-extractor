
from abc import ABC, abstractmethod

class BaseHandler(ABC):
    
    MEDIA_TYPE = None

    def __init__(self):
        self.info = {
            'media_type': self.MEDIA_TYPE,
        }

    @abstractmethod
    def get_meta_data(self, path, checksum):
        pass
