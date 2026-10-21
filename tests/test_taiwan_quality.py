from pathlib import Path
import unittest
from opencc_py import converter


class TaiwanQualityTests(unittest.TestCase):
    def test_quality_and_idempotence(self):
        for locale in ('tw2', 'twp'):
            convert = converter('cn', locale)
            for line in Path(__file__).with_name('taiwan-quality.tsv').read_text().splitlines():
                scope, source, expected = line.split('\t')
                if scope not in ('both', locale):
                    continue
                with self.subTest(locale=locale, source=source):
                    self.assertEqual(convert(source), expected)
                    self.assertEqual(convert(expected), expected)
                    self.assertNotIn('賬', expected)
                    self.assertNotIn('羣', expected)
