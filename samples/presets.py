from opencc_py import presets


def main() -> None:
    cn_to_tw = presets.cn2t.converter("cn", "tw2")
    tw_to_cn = presets.t2cn.converter("tw2", "cn")

    traditional = cn_to_tw("默认用户界面支持数据库和网络请求。")
    simplified = tw_to_cn(traditional)

    print(traditional)
    print(simplified)


if __name__ == "__main__":
    main()
