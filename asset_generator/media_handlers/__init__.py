"""
Media handlers provide an interface to different media storage types. This could
be standard POSIX, Object Store (S3, GCS, IPFS...), Tape, etc.

"""

from .object_store_handler import ObjectStoreHandler
from .posix_handler import PosixHandler
from .esgf_solr_handler import ESGFSolrHandler