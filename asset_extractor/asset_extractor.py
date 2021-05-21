from media_handlers.core.media_handler_picker import MediaHandlers

def process_file(media_type, path, checksum = None):
    media_handlers = MediaHandlers()
    media_handler = media_handlers.get_media_handler(media_type)(path, checksum)
    return media_handler.info


def main():
    # args = docopt.docopt(__doc__)
    media_type = 'posix'
    path = '/path/to/file.png'
    check_sum = 'checksum'
    print(process_file(media_type, path, check_sum))
    
if __name__ == '__main__':
    main()