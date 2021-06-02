from setuptools import setup, find_packages

with open("README.md") as readme_file:
    _long_description = readme_file.read()

setup(
    name='asset_extractor',
    description='Extracts file level metadata',
    author='Rhys Evans',
    url='https://github.com/cedadev/asset-extractor/',
    long_description=_long_description,
    long_description_content_type='text/markdown',
    license='BSD - See asset_extractor/LICENSE file for details',
    packages=find_packages(),
    package_data={
        'asset_extractor': [
            'LICENSE'
        ]
    },
    install_requires=[
        'python-magic',
    ],
    entry_points={
        'console_scripts': [
            'extract_assets = asset_extractor.scripts.extract_assets:main',
        ],
        'media_handlers': [
            'posix = asset_extractor.media_handlers:PosixHandler',
            'object_store = asset_extractor.media_handlers:ObjectStoreHandler',
        ],
        'output_backends': [
            'elasticsearch = asset_extractor.output_backends:ElasticsearchOutputBackend',
            'standard_out = asset_extractor.output_backends:StdoutOutputBackend'
        ],
        'input_plugins': [
            'file_system = asset_extractor.input_plugins:FileSystemInputPlugin'
        ]
    }
)
