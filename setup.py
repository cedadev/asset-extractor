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
        'asset_scanner',
        'boto3'
    ],
    extras_require={
        'docs': [
            'sphinx',
            'sphinx-rtd-theme',
            'sphinxcontrib-programoutput'
        ]
    },
    entry_points={
        'asset_extractor.media_handlers': [
            'POSIX = asset_extractor.media_handlers:PosixHandler',
            'OBJECT_STORE = asset_extractor.media_handlers:ObjectStoreHandler',
        ],
        'asset_scanner.extractors': [
            'asset_extractor = asset_extractor:AssetExtractor',
        ]
    }
)
