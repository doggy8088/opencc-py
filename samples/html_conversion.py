from opencc_py import HtmlConverter, converter


HTML = """
<html lang="zh-CN">
  <head>
    <meta name="description" content="默认用户界面支持数据库和网络请求。" />
  </head>
  <body>
    <p>软件开发和网络服务。</p>
    <p class="ignore-opencc">这段文字不会被转换。</p>
    <script>const text = "软件";</script>
  </body>
</html>
""".strip()


def main() -> None:
    convert = converter("cn", "tw2")
    html = HtmlConverter.from_xml_string(convert, HTML, "zh-CN", "zh-TW")

    html.convert()
    print(html.to_xml_string())

    html.restore()
    print(html.to_xml_string())


if __name__ == "__main__":
    main()
