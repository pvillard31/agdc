#__author__ = 'root'


"""
Ingester for landsat datasets.
"""
from __future__ import absolute_import

import logging

from agdc.ingest.landsat.core import LandsatIngester

_LOG = logging.getLogger(__name__)


from agdc.ingest import run_ingest
run_ingest(LandsatIngester)
