import os
from pathlib import Path
import tempfile

from autoreduce_utils.migrate_credentials import migrate_credentials


def test_migrate():
    with tempfile.TemporaryDirectory() as tempdir:
        migrate_credentials(tempdir)
        assert (Path(tempdir) / "credentials.ini").is_file()
