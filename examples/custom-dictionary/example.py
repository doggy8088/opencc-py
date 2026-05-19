from opencc_py import Dict, DictEntry, DictGroup, converter_factory, custom_converter, locale


custom_only = custom_converter(
    [
        DictEntry("香蕉", "banana"),
        DictEntry("蘋果", "apple"),
        DictEntry("用户", "使用者"),
        DictEntry("用户界面", "使用者介面"),
    ]
)

print(custom_only("香蕉、蘋果和用户界面"))

product_terms = Dict.from_entries(
    [
        DictEntry("預設使用者介面", "預設 UI"),
        DictEntry("資料庫", "DB"),
    ]
)

cn_to_tw_with_product_terms = converter_factory(
    locale.From.cn(),
    locale.To.tw2(),
    DictGroup([product_terms]),
)

print(cn_to_tw_with_product_terms("默认用户界面支持数据库和网络请求。"))
