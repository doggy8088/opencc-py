import unittest
from xml.etree import ElementTree

from opencc_py import HtmlConverter, custom_converter, html_converter


class HtmlConverterTests(unittest.TestCase):
    def test_convert_changes_text_and_attributes_when_lang_matches(self):
        root = self._build_document()
        converter = HtmlConverter(lambda s: s.upper(), root, "zh", "zh-Hant")

        converter.convert()

        self.assertEqual(root.attrib["lang"], "zh-Hant")
        self.assertEqual(root.find("./body/p").text, "HELLO")
        self.assertEqual(root.find("./head/meta[@name='description']").attrib["content"], "HELLO")
        self.assertEqual(root.find("./head/meta[@name='keywords']").attrib["content"], "KEYWORDS")
        self.assertEqual(root.find("./head/meta[@name='other']").attrib["content"], "ignore")
        self.assertEqual(root.find("./body/img").attrib["alt"], "HELLO")
        self.assertEqual(root.find("./body/input[@type='button']").attrib["value"], "HELLO")
        self.assertEqual(root.find("./body/input[@type='text']").attrib["value"], "hello")
        self.assertEqual(root.find("./body/div").text, "hello")
        self.assertEqual(root.find("./body/span").attrib["lang"], "en")
        self.assertEqual(root.find("./body/span").text, "hello")
        self.assertEqual(root.find("./body/script").text, "hello")
        self.assertEqual(root.find("./body/style").text, "hello")

    def test_restore_reverts_changes(self):
        root = self._build_document()
        converter = HtmlConverter(lambda s: s.upper(), root, "zh", "zh-Hant")

        converter.convert()
        converter.restore()

        self.assertEqual(root.attrib["lang"], "zh")
        self.assertEqual(root.find("./body/p").text, "hello")
        self.assertEqual(root.find("./head/meta[@name='description']").attrib["content"], "hello")
        self.assertEqual(root.find("./head/meta[@name='keywords']").attrib["content"], "keywords")
        self.assertEqual(root.find("./body/img").attrib["alt"], "hello")
        self.assertEqual(root.find("./body/input[@type='button']").attrib["value"], "hello")

    def test_from_xml_string_and_wrapper(self):
        converter = custom_converter("hello HELLO")
        html = HtmlConverter.from_xml_string(converter, "<html lang='zh'><body><p>hello</p></body></html>", "zh", "zh-Hant")
        html.convert()

        self.assertIn("HELLO", html.to_xml_string())

        root = ElementTree.fromstring("<html lang='zh'><body><p>hello</p></body></html>")
        wrapped = html_converter(converter, root, "zh", "zh-Hant")
        wrapped.convert()

        self.assertEqual(root.find("./body/p").text, "HELLO")

    def test_tail_text_uses_parent_lang_scope(self):
        root = ElementTree.fromstring("<p lang='zh'>hello<span lang='en'>hello</span>hello</p>")
        converter = HtmlConverter(lambda s: s.upper(), root, "zh", "zh-Hant")

        converter.convert()

        self.assertEqual(root.text, "HELLO")
        self.assertEqual(root.find("./span").text, "hello")
        self.assertEqual(root.find("./span").tail, "HELLO")

    @staticmethod
    def _build_document():
        xml = """<html lang="zh">
  <head>
    <meta name="description" content="hello" />
    <meta name="keywords" content="keywords" />
    <meta name="other" content="ignore" />
  </head>
  <body>
    <p>hello</p>
    <img alt="hello" />
    <input type="button" value="hello" />
    <input type="text" value="hello" />
    <div class="note ignore-opencc">hello</div>
    <span lang="en">hello</span>
    <script>hello</script>
    <style>hello</style>
  </body>
</html>"""
        return ElementTree.fromstring(xml)


if __name__ == "__main__":
    unittest.main()
