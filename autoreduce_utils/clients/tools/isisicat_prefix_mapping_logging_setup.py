# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
# pylint: skip-file
import logging
import logging.handlers
from pathlib import Path

from autoreduce_utils.settings import CONFIG_ROOT

LOGGING_LEVEL = logging.WARNING
logging_dir = Path(CONFIG_ROOT, 'logs')
logging_dir.mkdir(parents=True, exist_ok=True)
LOGGING_LOC = logging_dir / 'isisicat_prefix_mappings.log'

logger = logging.getLogger('IsisICATPrefixMappings')
logger.setLevel(LOGGING_LEVEL)
handler = logging.handlers.RotatingFileHandler(LOGGING_LOC, maxBytes=104857600, backupCount=20)
handler.setLevel(LOGGING_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
