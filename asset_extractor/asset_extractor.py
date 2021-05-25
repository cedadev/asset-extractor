from media_handlers.core.media_handler_picker import MediaHandlers

def process_file(media_type, path, checksum = None):
    media_handlers = MediaHandlers()
    media_handler = media_handlers.get_media_handler(media_type)()
    return media_handler.get_meta_data(path, checksum)


def main():
    media_type = 'posix'
    path = '/path/to/file.png'
    check_sum = {
        'time': 'datetime',
        'checksum': 'checksum'
    }
    print(process_file(media_type, path))
    
if __name__ == '__main__':
    main()