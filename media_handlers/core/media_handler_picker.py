import pkg_resources

class MediaHandlers:
    def __init__(self):
        self.media_handlers = {}
        for entry_point in pkg_resources.iter_entry_points('media_handlers'):
            self.media_handlers[entry_point.name] = entry_point.load()

    def get_media_handler(self, media_handler):
        return self.media_handlers[media_handler]
