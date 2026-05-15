from opencc_py import DictEntry, custom_converter


def main() -> None:
    convert = custom_converter(
        [
            DictEntry("OpenCC", "開放中文轉換"),
            DictEntry("软件", "軟體"),
            DictEntry("网络", "網路"),
        ]
    )

    print(convert("OpenCC 可以转换软件和网络相关词汇。"))

    punctuation = custom_converter("“ 「|” 」")
    print(punctuation("“OpenCC”"))


if __name__ == "__main__":
    main()
