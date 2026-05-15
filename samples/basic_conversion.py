from opencc_py import converter


def main() -> None:
    convert = converter("cn", "tw2")

    print(convert("汉语"))
    print(convert.convert("默认用户界面支持数据库和网络请求。"))


if __name__ == "__main__":
    main()
