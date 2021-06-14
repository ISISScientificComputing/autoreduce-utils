# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2019 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
"""
Command to move test_settings.py to settings.py
"""
import sys
import os
import logging
from shutil import copyfile
from pathlib import Path

from autoreduce_utils.settings import AUTOREDUCE_HOME_ROOT

logger = logging.getLogger(__package__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def migrate_credentials(destination_path: str):
    """
    Migrate the credentials.ini
    """
    utils_path = os.path.join(ROOT_DIR, 'autoreduce_utils')
    logger.info("================== Migrate credentials ====================")
    test_credentials_path = os.path.join(utils_path, 'test_credentials.ini')
    cred_dir = Path(destination_path).expanduser()
    cred_dir.mkdir(parents=True, exist_ok=True)
    credentials_path = cred_dir / "credentials.ini"
    logger.info("Copying credentials to %s", credentials_path)
    copyfile(test_credentials_path, credentials_path)
    logger.info("Credentials successfully migrated")


def main():
    """
    Entrypoint for the migrate credentials action
    """
    migrate_credentials(AUTOREDUCE_HOME_ROOT)


if __name__ == "__main__":
    main()
