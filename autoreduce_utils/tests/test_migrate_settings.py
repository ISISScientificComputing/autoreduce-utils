import os
from pathlib import Path
import tempfile

from autoreduce_utils.migrate_settings import migrate_settings


def test_migrate():
    with tempfile.TemporaryDirectory() as tempdir:
        migrate_settings(tempdir)
        assert (Path(tempdir) / "credentials.ini").is_file()
