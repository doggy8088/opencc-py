from opencc_py import converter


text = "鼠标和软件可以连接到计算机网络。"
shape_only = converter("cn", "t")
taiwan_words = converter("cn", "tw2")

print(f"原文：{text}")
print(f"只轉字形 cn -> t：{shape_only(text)}")
print(f"臺灣詞彙 cn -> tw2：{taiwan_words(text)}")
print()
print("差異：cn -> t 保留原本詞彙；cn -> tw2 會轉成臺灣慣用詞。")
