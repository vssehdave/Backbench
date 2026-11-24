import sys
import unittest
from pathlib import Path
import money

CATALOG = Path("strategies/catalog")


class CatalogChecks(unittest.TestCase):
    def test_every_manifest_loads(self):
        paths = sorted(CATALOG.glob("*/manifest.json"))
        self.assertGreaterEqual(len(paths), 5)
        for path in paths:
            sys.modules.pop("strategy", None)  # every folder names its module strategy.py
            with self.subTest(path=str(path)):
                money.load_manifest(path)

    def test_index_lists_every_folder(self):
        index = (CATALOG / "INDEX.md").read_text(encoding="utf-8")
        folders = [p.name for p in CATALOG.iterdir() if (p / "README.md").exists()]
        self.assertGreaterEqual(len(folders), 150)
        for name in folders:
            with self.subTest(folder=name):
                self.assertIn(f"]({name}/)", index)


if __name__ == "__main__":
    unittest.main()
