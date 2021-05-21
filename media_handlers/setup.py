from setuptools import setup

setup(
    name='media_handlers',
    entry_points={
        'console_scripts': [
            'media_handler_picker = core.media_handler_picker:main',
        ],
        'media_handlers': [
            'posix = posix_handler:PosixHandler',
            'object_store = object_store_handler:ObjectStoreHandler',
        ],
    }
)