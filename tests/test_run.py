import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from judgebench import run


class FakeJudge:
    name = "fake"

    def __init__(self, loaded):
        self.loaded = loaded

    def loaded_bytes(self):
        return self.loaded


class LoadedBytesTests(unittest.TestCase):
    def run_with(self, stored, loaded):
        with tempfile.TemporaryDirectory() as tmp:
            meta = Path(tmp) / "fake__meta.json"
            if stored is not None:
                meta.write_text(json.dumps({"loaded_bytes": stored}))
            with mock.patch.object(run, "RESULTS", Path(tmp)), \
                    mock.patch.object(run.judges, "make", return_value=FakeJudge(loaded)), \
                    mock.patch.object(run.datasets, "load", return_value=[]):
                run.run_judge("fake", ["honorific"])
            return json.loads(meta.read_text()).get("loaded_bytes")

    def test_a_judge_that_cannot_measure_keeps_the_stored_reading(self):
        self.assertEqual(self.run_with(123, None), 123)

    def test_a_new_reading_replaces_the_stored_one(self):
        self.assertEqual(self.run_with(123, 456), 456)

    def test_no_reading_anywhere_stays_absent(self):
        self.assertIsNone(self.run_with(None, None))


if __name__ == "__main__":
    unittest.main()
