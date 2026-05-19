from opencc_py import HtmlConverter, converter


xml = """
<html lang="zh-HK">
  <body>
    <h1>漢語轉換示例</h1>
    <p lang="zh-HK">伺服器與網絡服務已啟動。</p>
    <p lang="en">This paragraph should stay unchanged.</p>
  </body>
</html>
"""

convert = converter("hk", "cn")
html = HtmlConverter.from_xml_string(convert, xml, "zh-HK", "zh-CN")

html.convert()
print("轉換後：")
print(html.to_xml_string())

html.restore()
print()
print("還原後：")
print(html.to_xml_string())
