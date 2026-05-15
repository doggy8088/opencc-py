import unittest

from opencc_py import DictEntry, Trie


class TrieTests(unittest.TestCase):
    def test_convert_uses_longest_match(self):
        trie = Trie()
        trie.add_word("ab", "X")
        trie.add_word("a", "Y")

        self.assertEqual(trie.convert("abca"), "XcY")

    def test_load_dict_skips_malformed_lines(self):
        trie = Trie()
        trie.load_dict("a b|invalid|c d|Web 平台庫\tWeb 平台函式庫")

        self.assertEqual(trie.convert("a"), "b")
        self.assertEqual(trie.convert("c"), "d")
        self.assertEqual(trie.convert("Web 平台庫"), "Web 平台函式庫")
        self.assertEqual(trie.convert("x"), "x")

    def test_load_entries(self):
        trie = Trie()
        trie.load_entries([DictEntry("香蕉", "banana"), ("蘋果", "apple")])

        self.assertEqual(trie.convert("香蕉和蘋果"), "banana和apple")

    def test_convert_handles_astral_code_points(self):
        trie = Trie()
        trie.add_word("🚀发布", "🚀發表")
        trie.add_word("发布", "發表")

        self.assertEqual(trie.convert("🚀发布数据库"), "🚀發表数据库")

    def test_none_arguments_raise(self):
        trie = Trie()

        with self.assertRaises(TypeError):
            trie.add_word(None, "target")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            trie.add_word("source", None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            trie.load_dict(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            trie.convert(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
