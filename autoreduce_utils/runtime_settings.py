# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2019 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
# pylint: skip-file
import os

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
