from setuptools import setup, find_packages

with open("README.md") as readme_file:
    _long_description = readme_file.read()

setup(
    name='asset_generator',
    description='Extracts file level metadata',
    author='Rhys Evans',
    url='https://github.com/cedadev/asset-generator/',
    long_description=_long_description,
    long_description_content_type='text/markdown',
    license='BSD - See asset_generator/LICENSE file for details',
    packages=find_packages(),
    package_data={
        'asset_generator': [
            'LICENSE'
        ]
    },
    install_requires=[
        'python-magic',
        'asset_scanner',
    ],
    extras_require={
        'docs': [
            'sphinx',
            'sphinx-rtd-theme',
            'sphinxcontrib-programoutput'
        ],
        's3': [
           'boto3'
        ]
    },
    entry_points={
        'asset_generator.media_handlers': [
            'POSIX = asset_generator.media_handlers:PosixHandler',
            'OBJECT_STORE = asset_generator.media_handlers:ObjectStoreHandler',
            'ESGF_SOLR = asset_generator.media_handlers:ESGFSolrHandler'
        ],
        'asset_scanner.extractors': [
            'asset_generator = asset_generator:AssetExtractor',
        ]
    }
)
