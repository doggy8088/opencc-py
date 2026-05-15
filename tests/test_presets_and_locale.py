import unittest

from opencc_py import locale, presets
from opencc_py.core import OpenCCError


class PresetsAndLocaleTests(unittest.TestCase):
    def test_locale_maps_contain_expected_keys(self):
        self.assertEqual(set(locale.from_map()), {"cn", "hk", "tw", "tw2", "twp", "jp"})
        self.assertEqual(set(locale.to_map()), {"cn", "hk", "tw", "tw2", "twp", "jp"})
        self.assertGreater(len(locale.From.cn()), 0)
        self.assertGreater(len(locale.To.cn()), 0)

    def test_full_preset_accepts_all_directions(self):
        self.assertEqual(presets.full.converter("cn", "tw2").convert("汉语"), "漢語")
        self.assertEqual(presets.full.converter("tw", "cn").convert("漢語"), "汉语")

    def test_cn2t_preset_restricts_supported_directions(self):
        self.assertEqual(presets.cn2t.converter("cn", "tw2").convert("汉语"), "漢語")
        with self.assertRaises(OpenCCError):
            presets.cn2t.converter("tw", "cn")

    def test_t2cn_preset_restricts_supported_directions(self):
        self.assertEqual(presets.t2cn.converter("tw2", "cn").convert("漢語"), "汉语")
        with self.assertRaises(OpenCCError):
            presets.t2cn.converter("cn", "tw")


if __name__ == "__main__":
    unittest.main()
