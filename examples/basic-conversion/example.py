from opencc_py import converter


convert = converter("cn", "tw2")

for text in [
    "汉语是一种美丽的语言。",
    "默认用户界面支持数据库和网络请求。",
    "这只鼠标连接到计算机后，可以打开软件设置。",
]:
    print(f"原文：{text}")
    print(f"轉換：{convert(text)}")
    print()
