import subprocess
import sys
import unittest
from pathlib import Path

from opencc_py import dict_data


class DictDataTests(unittest.TestCase):
    def test_generated_metadata_contains_expected_dictionaries(self):
        expected = {
            "HK_VARIANTS",
            "HK_VARIANTS_REV",
            "HK_VARIANTS_REV_PHRASES",
            "JP_SHINJITAI_CHARACTERS",
            "JP_SHINJITAI_PHRASES",
            "JP_VARIANTS",
            "JP_VARIANTS_REV",
            "ST_CHARACTERS",
            "ST_PHRASES",
            "TS_CHARACTERS",
            "TS_PHRASES",
            "TW_PHRASES_CUSTOM",
            "TW_PHRASES_CUSTOM_REV",
            "TW_PHRASES_IT",
            "TW_PHRASES_NAME",
            "TW_PHRASES_OTHER",
            "TW_PHRASES_REV",
            "TW_VARIANTS",
            "TW_VARIANTS_REV",
            "TW_VARIANTS_REV_PHRASES",
        }

        self.assertEqual(set(dict_data.DICT_METADATA), expected)
        self.assertGreater(dict_data.DICT_METADATA["ST_CHARACTERS"]["entries"], 0)
        self.assertGreater(dict_data.DICT_METADATA["TW_PHRASES_CUSTOM"]["entries"], 0)

    def test_generator_is_deterministic(self):
        project_root = Path(__file__).resolve().parents[1]
        source = project_root.parent / "OpenCC" / "src" / "OpenCC" / "Internal" / "DictData.cs"
        if not source.exists():
            self.skipTest("C# DictData.cs source is not available in this checkout.")

        current = project_root / "src" / "opencc_py" / "dict_data.py"
        target = project_root / "build" / "test-dict-data.py"
        target.parent.mkdir(exist_ok=True)

        subprocess.run(
            [sys.executable, "tools/generate_dict_data.py", "--output", str(target)],
            cwd=project_root,
            check=True,
        )

        self.assertEqual(target.read_text(encoding="utf-8"), current.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
