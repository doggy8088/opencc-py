from __future__ import annotations

from . import dict_data
from .core import DictGroup, LocalePreset

TW_PHRASES_CUSTOM_ADDITIONS = (
    "網絡服務\t網路服務|應用程序網關\t應用程式閘道|鏡像文件\t映像檔|保存更改\t儲存變更|儲存更改\t儲存變更|"
    "文件名\t檔名|文件系統\t檔案系統|文件描述符\t檔案描述子|函數調用\t函式呼叫|渲染管線\t算繪管線|內存分配\t記憶體配置|"
    "網絡棧\t網路堆疊|網絡適配器\t網路介面卡"
)

TW_PHRASES_CUSTOM_ADDITIONS_REV = (
    "網路服務\t網絡服務|應用程式閘道\t應用程序網關|映像檔\t鏡像文件|儲存變更\t儲存更改|"
    "檔名\t文件名|檔案系統\t文件系統|檔案描述子\t文件描述符|函式呼叫\t函數調用|算繪管線\t渲染管線|記憶體配置\t內存分配|"
    "網路堆疊\t網絡棧|網路介面卡\t網絡適配器"
)


def from_cn() -> DictGroup:
    return DictGroup.from_strings(dict_data.ST_CHARACTERS, dict_data.ST_PHRASES)


def from_hk() -> DictGroup:
    return DictGroup.from_strings(dict_data.HK_VARIANTS_REV, dict_data.HK_VARIANTS_REV_PHRASES)


def from_tw() -> DictGroup:
    return DictGroup.from_strings(dict_data.TW_VARIANTS_REV, dict_data.TW_VARIANTS_REV_PHRASES)


def from_tw2() -> DictGroup:
    return DictGroup.from_strings(
        dict_data.TW_VARIANTS_REV,
        dict_data.TW_PHRASES_CUSTOM_REV,
        TW_PHRASES_CUSTOM_ADDITIONS_REV,
    )


def from_twp() -> DictGroup:
    return DictGroup.from_strings(
        dict_data.TW_VARIANTS_REV,
        dict_data.TW_VARIANTS_REV_PHRASES,
        dict_data.TW_PHRASES_REV,
    )


def from_jp() -> DictGroup:
    return DictGroup.from_strings(
        dict_data.JP_VARIANTS_REV,
        dict_data.JP_SHINJITAI_CHARACTERS,
        dict_data.JP_SHINJITAI_PHRASES,
    )


def to_cn() -> DictGroup:
    return DictGroup.from_strings(dict_data.TS_CHARACTERS, dict_data.TS_PHRASES)


def to_hk() -> DictGroup:
    return DictGroup.from_strings(dict_data.HK_VARIANTS)


def to_tw() -> DictGroup:
    return DictGroup.from_strings(dict_data.TW_VARIANTS)


def to_tw2() -> DictGroup:
    return DictGroup.from_strings(
        dict_data.TW_VARIANTS,
        dict_data.TW_PHRASES_CUSTOM,
        TW_PHRASES_CUSTOM_ADDITIONS,
    )


def to_twp() -> DictGroup:
    return DictGroup.from_strings(
        dict_data.TW_VARIANTS,
        dict_data.TW_PHRASES_IT,
        dict_data.TW_PHRASES_NAME,
        dict_data.TW_PHRASES_OTHER,
    )


def to_jp() -> DictGroup:
    return DictGroup.from_strings(dict_data.JP_VARIANTS)


def from_map() -> dict[str, DictGroup]:
    return {
        "cn": from_cn(),
        "hk": from_hk(),
        "tw": from_tw(),
        "tw2": from_tw2(),
        "twp": from_twp(),
        "jp": from_jp(),
    }


def to_map() -> dict[str, DictGroup]:
    return {
        "cn": to_cn(),
        "hk": to_hk(),
        "tw": to_tw(),
        "tw2": to_tw2(),
        "twp": to_twp(),
        "jp": to_jp(),
    }


def full_preset() -> LocalePreset:
    return LocalePreset(from_map(), to_map())


def cn2t_preset() -> LocalePreset:
    return LocalePreset(
        {"cn": from_cn()},
        {
            "hk": to_hk(),
            "tw": to_tw(),
            "tw2": to_tw2(),
            "twp": to_twp(),
            "jp": to_jp(),
        },
    )


def t2cn_preset() -> LocalePreset:
    return LocalePreset(
        {
            "hk": from_hk(),
            "tw": from_tw(),
            "tw2": from_tw2(),
            "twp": from_twp(),
            "jp": from_jp(),
        },
        {"cn": to_cn()},
    )
