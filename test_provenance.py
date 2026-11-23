import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from harness import engine_digest


class ProvenanceTests(unittest.TestCase):
    def test_content_digest_handles_relocation_and_detects_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            left, right = Path(tmp, "left"), Path(tmp, "right")
            left.mkdir()
            right.mkdir()
            for name in ("harness.py", "stress.py"):
                (left / name).write_bytes(b"first\nsecond\n")
                (right / name).write_bytes(b"first\r\nsecond\r\n")
            reference = engine_digest(left)
            self.assertEqual(reference, engine_digest(right))
            for name in ("harness.py", "stress.py"):
                (right / name).write_bytes(b"changed\n")
                self.assertNotEqual(reference, engine_digest(right))
                (right / name).write_bytes(b"first\nsecond\n")

    def test_cli_contract_omits_local_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "report.json")
            subprocess.run([sys.executable, str(Path(__file__).with_name("harness.py")),
                            "--out", str(path), "--paths", "1"], check=True)
            result = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(result["execution_contract"]["engine_sha256"], engine_digest())
            self.assertFalse({"minute_csv", "provider", "out"} & result["config"].keys())
