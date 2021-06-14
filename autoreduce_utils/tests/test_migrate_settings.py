# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
import tempfile
from pathlib import Path
from autoreduce_utils.migrate_credentials import migrate_credentials


def test_migrate():
    """
    Test that the credentials are migrated
    """
    with tempfile.TemporaryDirectory() as tempdir:
        migrate_credentials(tempdir)
        assert (Path(tempdir) / "credentials.ini").is_file()
