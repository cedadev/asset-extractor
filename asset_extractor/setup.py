from setuptools import setup

setup(
    name='asset_extractor',
    entry_points={
        'console_scripts': [
            'asset_extractor = asset_extractor:main',
        ],
    }
)