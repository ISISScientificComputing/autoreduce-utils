# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
# pylint: skip-file
"""
Settings for connecting to the test services that run locally
"""
import configparser
import os
from pathlib import Path

from autoreduce_utils.clients.settings.client_settings_factory import ClientSettingsFactory

FACILITY = 'ISIS'

AUTOREDUCE_HOME_ROOT = os.environ.get("AUTOREDUCTION_USERDIR", os.path.expanduser("~/.autoreduce"))

os.makedirs(os.path.join(AUTOREDUCE_HOME_ROOT, "logs"), exist_ok=True)

LOG_LEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
LOG_FILE = os.path.join(AUTOREDUCE_HOME_ROOT, 'logs', 'autoreduce.log')

CREDENTIALS_INI_FILE = os.environ.get("AUTOREDUCTION_CREDENTIALS",
                                      os.path.expanduser(f"{AUTOREDUCE_HOME_ROOT}/credentials.ini"))

PROJECT_DEV_ROOT = os.path.join(AUTOREDUCE_HOME_ROOT, "dev")
os.makedirs(PROJECT_DEV_ROOT, exist_ok=True)

# The reduction outputs are copied here on completion. They are saved in /tmp/<randomdir>
# sa the reduction is running. By default the output is also saved locally
# unless AUTOREDUCTION_PRODUCTION is specified
CEPH_DIRECTORY = f"{PROJECT_DEV_ROOT}/reduced-data/%s/RB%s/autoreduced/%s/"

if "AUTOREDUCTION_PRODUCTION" in os.environ:
    # for when deploying on production - this is the real path where the mounts are
    ARCHIVE_ROOT = "\\\\isis\\inst$\\" if os.name == "nt" else "/isis"
    CEPH_DIRECTORY = "/instrument/%s/RBNumber/RB%s/autoreduced/%s"
elif "RUNNING_VIA_PYTEST" in os.environ:
    # For testing which uses a local folder to simulate an archive. It's nice for this
    # to be different than the development one, otherwise running the tests will delete
    # any manual changes you've done to the archive folder, e.g. for testing reduction scripts
    ARCHIVE_ROOT = os.path.join(PROJECT_DEV_ROOT, 'test-archive')
else:
    # the default development path
    ARCHIVE_ROOT = os.path.join(PROJECT_DEV_ROOT, 'data-archive')

MANTID_PATH = "/opt/Mantid/lib"

# The path is structured as follows. The %s fill out the instrument name and the cycle number
CYCLE_DIRECTORY = os.path.join(ARCHIVE_ROOT, 'NDX%s', 'Instrument', 'data', 'cycle_%s')
SCRIPTS_DIRECTORY = os.path.join(ARCHIVE_ROOT, "NDX%s", "user", "scripts", "autoreduction")

SCRIPT_TIMEOUT = 3600  # The max time to wait for a user script to finish running (seconds)
TEMP_ROOT_DIRECTORY = "/autoreducetmp"

CONFIG = configparser.ConfigParser()
CONFIG.read(CREDENTIALS_INI_FILE)


def get_setting(section: str, key: str) -> str:
    """
    Gets the value of the key from the section.
    """
    return str(CONFIG.get(section, key, raw=True))  # raw=True to allow strings with special characters to be passed


SETTINGS_FACTORY = ClientSettingsFactory()

ICAT_SETTINGS = SETTINGS_FACTORY.create('icat',
                                        username=get_setting('ICAT', 'user'),
                                        password=get_setting('ICAT', 'password'),
                                        host=get_setting('ICAT', 'host'),
                                        port='',
                                        authentication_type=get_setting('ICAT', 'auth'))

MYSQL_SETTINGS = SETTINGS_FACTORY.create('database',
                                         username=get_setting('DATABASE', 'user'),
                                         password=get_setting('DATABASE', 'password'),
                                         host=get_setting('DATABASE', 'host'),
                                         port=get_setting('DATABASE', 'port'),
                                         database_name=get_setting('DATABASE', 'name'))

ACTIVEMQ_SETTINGS = SETTINGS_FACTORY.create('queue',
                                            username=get_setting('QUEUE', 'user'),
                                            password=get_setting('QUEUE', 'password'),
                                            host=get_setting('QUEUE', 'host'),
                                            port=get_setting('QUEUE', 'port'))

LOCAL_MYSQL_SETTINGS = SETTINGS_FACTORY.create('database',
                                               username=get_setting('DATABASE', 'user'),
                                               password=get_setting('DATABASE', 'password'),
                                               host=get_setting('DATABASE', 'host'),
                                               port=get_setting('DATABASE', 'port'))

SFTP_SETTINGS = SETTINGS_FACTORY.create('sftp',
                                        username=get_setting('SFTP', 'user'),
                                        password=get_setting('SFTP', 'password'),
                                        host=get_setting('SFTP', 'host'),
                                        port=get_setting('SFTP', 'port'))

CYCLE_SETTINGS = SETTINGS_FACTORY.create('cycle',
                                         username=get_setting('CYCLE', 'user'),
                                         password=get_setting('CYCLE', 'password'),
                                         host='',
                                         port='',
                                         uows_url=get_setting('CYCLE', 'uows_url'),
                                         scheduler_url=get_setting('CYCLE', 'scheduler_url'))
