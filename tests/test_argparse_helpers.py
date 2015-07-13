# coding: spec

from delfick_app import DelayedFileType, ArgumentError

from delfick_error import DelfickErrorTestMixin
from unittest import TestCase
import tempfile
import argparse
import shutil
import uuid
import nose
import sys
import os

class TestCase(TestCase, DelfickErrorTestMixin): pass

describe TestCase, "DelayedFileType":
    it "does nothing to the file if it's already a file":
        filename = None
        try:
            filename = tempfile.NamedTemporaryFile(delete=False).name
            fle = open(filename)
            self.assertIs(DelayedFileType("r")(fle)(), fle)
        finally:
            if filename and os.path.exists(filename):
                os.remove(filename)

    it "opens the file if it exists":
        filename = None
        try:
            content = str(uuid.uuid1())
            filename = tempfile.NamedTemporaryFile(delete=False).name
            with open(filename, "w") as fle:
                fle.write(content)
            self.assertEqual(DelayedFileType("r")(filename)().read().strip(), content)
        finally:
            if filename and os.path.exists(filename):
                os.remove(filename)

    it "complains if the file is not a file":
        filename = None
        try:
            content = str(uuid.uuid1())
            filename = tempfile.mkdtemp()
            delayed = DelayedFileType("r")(filename)

            with self.fuzzyAssertRaisesError(ArgumentError, "Failed to open the file", error=str(IOError(21, "Is a directory")), location=filename):
                delayed()
        finally:
            if filename and os.path.exists(filename):
                shutil.rmtree(filename)

    it "complains if the file is not readable":
        filename = None
        try:
            content = str(uuid.uuid1())
            filename = tempfile.NamedTemporaryFile(delete=False).name
            delayed = DelayedFileType("r")(filename)

            os.chmod(filename, 0x447)

            with self.fuzzyAssertRaisesError(ArgumentError, "Failed to open the file", error=str(IOError(13, "Permission denied")), location=filename):
                delayed()
        finally:
            if filename and os.path.exists(filename):
                os.remove(filename)

    it "can be used with argparse":
        filename1 = None
        filename2 = None
        try:
            content = str(uuid.uuid1())
            filename1 = tempfile.NamedTemporaryFile(delete=False).name
            filename2 = tempfile.NamedTemporaryFile(delete=False).name
            with open(filename2, 'w') as fle:
                fle.write(content)
            os.remove(filename1)

            parser = argparse.ArgumentParser(description="test")
            parser.add_argument("--config"
                , help = "the config file!"
                , default = filename1
                , type = DelayedFileType('r')
                )

            args = parser.parse_args(["--config", filename2])
            self.assertEqual(args.config().read().strip(), content)
        finally:
            if filename1 and os.path.exists(filename1):
                os.remove(filename1)
            if filename2 and os.path.exists(filename2):
                os.remove(filename2)

    it "fails with normal FileType in Python2.6":
        if type(sys.version_info) is not tuple:
            raise nose.SkipTest()

        filename1 = None
        filename2 = None
        try:
            content = str(uuid.uuid1())
            filename1 = tempfile.NamedTemporaryFile(delete=False).name
            filename2 = tempfile.NamedTemporaryFile(delete=False).name
            with open(filename2, 'w') as fle:
                fle.write(content)
            os.remove(filename1)

            parser = argparse.ArgumentParser(description="test")
            parser.add_argument("--config"
                , help = "the config file!"
                , default = filename1
                , type = argparse.FileType('r')
                )

            with self.fuzzyAssertRaisesError(IOError, ".*\[Errno 2\] No such file or directory.+"):
                args = parser.parse_args(["--config", filename2])
        finally:
            if filename1 and os.path.exists(filename1):
                os.remove(filename1)
            if filename2 and os.path.exists(filename2):
                os.remove(filename2)

