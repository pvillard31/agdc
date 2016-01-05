#!/usr/bin/env python

# ===============================================================================
# Copyright 2015 Geoscience Australia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

"""
Ingester for Moisture percentile datasets.
"""
from __future__ import absolute_import

import logging

from .core import MoisturePercentileIngester

_LOG = logging.getLogger(__name__)


def cli():
    from agdc.ingest import run_ingest
    run_ingest(MoisturePercentileIngester)
