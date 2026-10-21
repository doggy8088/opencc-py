import unittest

from opencc_py import dict_data
from opencc_py import (
    ConverterOptions,
    Dict,
    DictEntry,
    DictGroup,
    LocalePreset,
    OpenCCError,
    converter,
    converter_builder,
    converter_factory,
    custom_converter,
)


class ConverterTests(unittest.TestCase):
    def test_converter_factory_converts_sequentially(self):
        group1 = DictGroup.from_entries([DictEntry("a", "b")])
        group2 = DictGroup.from_entries([DictEntry("b", "c")])

        self.assertEqual(converter_factory(group1, group2).convert("a"), "c")
        self.assertEqual(converter_factory([group1, group2]).convert("a"), "c")

    def test_converter_builder_reports_missing_and_unknown_locales(self):
        builder = converter_builder(self._preset())

        with self.assertRaisesRegex(OpenCCError, "Please provide the `from` option"):
            builder(ConverterOptions("", "to"))
        with self.assertRaisesRegex(OpenCCError, "Unknown locale `missing` for `from` option"):
            builder(ConverterOptions("missing", "to"))

    def test_converter_builder_supports_passthrough_t(self):
        builder = converter_builder(self._preset())

        self.assertEqual(builder(ConverterOptions("t", "to")).convert("b"), "c")
        self.assertEqual(builder(ConverterOptions("from", "t")).convert("a"), "b")

    def test_custom_converter_supports_raw_entries_and_mapping(self):
        raw = custom_converter("香蕉 banana|蘋果 apple|梨 pear")
        entries = custom_converter([DictEntry("banana", "香蕉"), ("apple", "蘋果")])
        mapping = custom_converter({"pear": "梨"})

        self.assertEqual(raw("香蕉 蘋果 梨"), "banana apple pear")
        self.assertEqual(entries("banana apple"), "香蕉 蘋果")
        self.assertEqual(mapping("pear"), "梨")

    def test_builtin_converter_converts_cn_to_tw2_preferred_terms(self):
        conv = converter("cn", "tw2")
        cases = [
            ("汉语", "漢語"),
            ("台湾", "台灣"),
            ("电子邮件", "電子郵件"),
            ("视频", "影片"),
            ("音频", "音訊"),
            ("软件", "軟體"),
            ("硬件", "硬體"),
            ("程序", "程式"),
            ("进程", "行程"),
            ("进程间通信", "行程間通訊"),
            ("线程", "執行緒"),
            ("数据", "資料"),
            ("数据库", "資料庫"),
            ("网络服务", "網路服務"),
            ("应用程序网关", "應用程式閘道"),
            ("镜像文件", "映像檔"),
            ("保存更改", "儲存變更"),
            ("网络", "網路"),
            ("信息", "資訊"),
            ("质量", "質量"),
            ("用户", "使用者"),
            ("默认", "預設"),
            ("创建", "建立"),
            ("实现", "實作"),
            ("运行", "執行"),
            ("发布", "發表"),
            ("屏幕", "螢幕"),
            ("界面", "介面"),
            ("文档", "文件"),
            ("操作系统", "作業系統"),
            ("剑指", "針對"),
            ("痛点", "要害"),
            ("硬伤", "罩門"),
        ]

        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(conv.convert(source), expected)

    def test_builtin_converter_preserves_cn_to_tw2_generic_item_terms(self):
        conv = converter("cn", "tw2")
        cases = [
            ("项目", "項目"),
            ("項目", "項目"),
            ("清单项目", "清單項目"),
            ("每个项目", "每個項目"),
        ]

        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(conv.convert(source), expected)

    def test_builtin_converter_converts_cn_to_tw2_project_context_compounds(self):
        conv = converter("cn", "tw2")
        cases = [
            ("项目文件夹", "專案資料夾"),
            ("项目的", "項目的"),
            ("项目目录", "專案目錄"),
            ("项目管理", "項目管理"),
            ("项目设置", "專案設定"),
        ]

        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(conv.convert(source), expected)

    def test_builtin_converter_converts_sentence_and_edge_cases(self):
        conv = converter("cn", "tw2")
        cases = [
            ("命令行工具", "命令列工具"),
            ("数据结构数据库", "資料結構資料庫"),
            ("响应式编程响应头", "回應式程式設計回應標頭"),
            ("进程间通信和多线程", "行程間通訊和多執行緒"),
            ("文件名和文件系统", "檔名和檔案系統"),
            ("文件描述符和函数调用", "檔案描述子和函式呼叫"),
            ("渲染管线和内存分配", "算繪管線和記憶體配置"),
            ("网络栈和网络适配器", "網路堆疊和網路介面卡"),
            ("Web 平台库", "Web 平台函式庫"),
            ("for 循环和while 循环", "for 迴圈和while 迴圈"),
            ("元数据 API", "Metadata API"),
            ("类（ Class ）加载器", "類別（ Class ）載入器"),
            ("“数据库”, “网络请求”", "“資料庫”, “網路請求”"),
            ("项目设置：默认值", "專案設定：預設值"),
            ("「类」", "「類別」"),
            ("类。", "類別。"),
            ("（视频）", "（影片）"),
            ("软件发布", "軟體發表"),
            ("发布响应式编程教程", "發表回應式程式設計課程"),
            ("发布数据库迁移脚本", "發表資料庫遷移指令碼"),
            ("千钧一发", "千鈞一髮"),
            ("一触即发", "一觸即發"),
            ("百发百中", "百發百中"),
            ("爆发发布", "爆發發表"),
            ("台湾台球桌", "台灣撞球桌"),
            ("折叠粘土", "折疊黏土"),
            ("鼠标事件", "滑鼠事件"),
            ("菜单链接账户账号", "選單連結帳戶帳號"),
            ("默认用户界面支持数据库和网络请求。", "預設使用者介面支援資料庫和網路請求。"),
            ("命令行工具加载配置文件。", "命令列工具載入組態檔。"),
            ("创建软件项目目录和项目设置。", "建立軟體專案目錄和專案設定。"),
            ("调试器显示调用堆栈和断点。", "偵錯工具顯示呼叫堆疊和中斷點。"),
            ("程序员重构代码库并发布版本。", "程式設計師重構程式碼庫並發表版本。"),
            ("响应式编程教程包含缓存策略。", "回應式程式設計課程包含快取策略。"),
            ("数据库🚀网络请求", "資料庫🚀網路請求"),
        ]

        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(conv.convert(source), expected)

    def test_builtin_converter_converts_tw2_back_to_cn(self):
        conv = converter("tw2", "cn")
        cases = [
            ("檔名和檔案系統", "文件名和文件系统"),
            ("檔案描述子和函式呼叫", "文件描述符和函数调用"),
            ("算繪管線和記憶體配置", "渲染管线和内存分配"),
            ("網路堆疊和網路介面卡", "网络栈和网络适配器"),
        ]

        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(conv.convert(source), expected)

    def test_builtin_converter_preserves_standalone_project_and_converts_compounds_to_cn(self):
        conv = converter("tw2", "cn")
        cases = [
            ("專案", "专案"),
            ("專案設定", "项目设置"),
            ("專案目錄", "项目目录"),
            ("專案管理", "项目管理"),
            ("專案資料夾", "项目文件夹"),
            ("專案的", "项目的"),
        ]

        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(conv.convert(source), expected)

    def test_builtin_converter_rewrites_ping_tai_to_ping_tai_in_tw2(self):
        """tw2 should consistently prefer 平台 over 平臺 for all platform-related terms."""
        conv = converter("cn", "tw2")
        cases = [
            # bare 平台 (simplified) should stay 平台 (not become 平臺)
            ("平台", "平台"),
            # common compound terms
            ("跨平台", "跨平台"),
            ("软件平台", "軟體平台"),
            ("作业平台", "作業平台"),
            # library-compound terms still expand 庫→函式庫
            ("Web 平台库", "Web 平台函式庫"),
            ("全平台库列表", "全平台函式庫列表"),
            ("原生平台库", "原生平台函式庫"),
        ]

        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(conv.convert(source), expected)

    def test_builtin_converter_rewrites_tw2_ping_tai_back_to_ping_tai_in_cn(self):
        """tw2→cn reverse: 平台 in tw2 context maps back to 平台 in cn."""
        conv = converter("tw2", "cn")
        cases = [
            ("跨平台", "跨平台"),
            ("軟體平台", "软件平台"),
        ]

        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(conv.convert(source), expected)

    def test_builtin_converter_uses_tai_except_official_names_in_tw2(self):
        """tw2 uses 台 in everyday words and keeps 臺 in official names."""
        conv = converter("cn", "tw2")
        cases = [
            # 日常用語用「台」
            ("台北", "台北"),
            ("台湾", "台灣"),
            ("台中", "台中"),
            ("台阶", "台階"),
            ("电视台", "電視台"),
            ("舞台", "舞台"),
            ("后台", "後台"),
            ("台积电", "台積電"),
            # 「颱」「檯」不受影響
            ("台风", "颱風"),
            ("柜台", "櫃檯"),
            ("吧台", "吧檯"),
            ("台灯", "檯燈"),
            # 正式名稱保留「臺」
            ("国立台湾大学", "國立臺灣大學"),
            ("台北市政府", "臺北市政府"),
            ("新台币", "新臺幣"),
            ("台湾银行", "臺灣銀行"),
            ("台湾台北地方法院", "臺灣臺北地方法院"),
            ("我在台北市政府上班", "我在臺北市政府上班"),
        ]

        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(conv.convert(source), expected)

    def test_builtin_converter_normalizes_tai_in_tw2_official_names(self):
        cases = [
            ("tw", "tw2", "臺北", "台北"),
            ("tw", "tw2", "國立臺灣大學", "國立臺灣大學"),
            # 寫成「台」的正式名稱統一成「臺」
            ("tw2", "tw2", "台北市政府", "臺北市政府"),
            ("tw2", "tw2", "新台幣", "新臺幣"),
            ("tw2", "tw2", "台灣臺北地方法院", "臺灣臺北地方法院"),
            ("tw2", "cn", "國立臺灣大學", "国立台湾大学"),
            ("tw2", "cn", "台北", "台北"),
        ]

        for source_locale, target_locale, source, expected in cases:
            with self.subTest(source=source, source_locale=source_locale, target_locale=target_locale):
                self.assertEqual(converter(source_locale, target_locale).convert(source), expected)

    def test_builtin_converter_keeps_every_tw2_tai_proper_noun_in_context(self):
        proper_nouns = sorted(
            {line.split("\t")[1] for line in dict_data.TW_2_TAI.splitlines() if line.strip()} - {"台"}
        )
        cn_to_tw2 = converter("cn", "tw2")
        tw2_to_cn = converter("tw2", "cn")
        tw_to_tw2 = converter("tw", "tw2")
        tw2_to_tw2 = converter("tw2", "tw2")

        self.assertTrue(proper_nouns)
        for noun in proper_nouns:
            text = f"在{noun}前"
            with self.subTest(noun=noun):
                self.assertEqual(cn_to_tw2.convert(tw2_to_cn.convert(text)), text)
                self.assertEqual(tw_to_tw2.convert(text), text)
                self.assertEqual(tw2_to_tw2.convert(text), text)

    @staticmethod
    def _preset():
        return LocalePreset(
            {"from": DictGroup([Dict.from_entries([DictEntry("a", "b")])])},
            {"to": DictGroup([Dict.from_entries([DictEntry("b", "c")])])},
        )


if __name__ == "__main__":
    unittest.main()
