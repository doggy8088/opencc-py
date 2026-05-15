from __future__ import annotations

from ..core import Converter, ConverterOptions, LocalePreset, converter_builder
from ..locale_data import t2cn_preset


def locale() -> LocalePreset:
    return t2cn_preset()


def converter(from_: str, to: str) -> Converter:
    return converter_with_options(ConverterOptions(from_, to))


def converter_with_options(options: ConverterOptions) -> Converter:
    return converter_builder(locale())(options)
