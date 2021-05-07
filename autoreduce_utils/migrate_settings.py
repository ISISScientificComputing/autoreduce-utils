# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2019 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
"""
Command to move test_settings.py to settings.py
"""
import os
import logging
from shutil import copyfile
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def migrate_settings(destination_path: str):
    utils_path = os.path.join(ROOT_DIR, 'autoreduce_utils')
    logging.info("================== Migrate credentials ====================")
    test_credentials_path = os.path.join(utils_path, 'test_credentials.ini')
    cred_dir = Path(destination_path).expanduser()
    cred_dir.mkdir(parents=True, exist_ok=True)
    credentials_path = cred_dir / "credentials.ini"
    logging.info(f"Copying credentials to {credentials_path}")
    try:
        copyfile(test_credentials_path, credentials_path)
    except OSError as error:
        logging.error(error)
        raise

    logging.info("Credentials successfully migrated\n")


def main():
    destination_path = "~/.autoreduce/"
    migrate_settings(destination_path)