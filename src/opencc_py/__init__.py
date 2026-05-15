"""Pure Python OpenCC converter."""

from . import locale, presets
from .core import (
    Converter,
    ConverterOptions,
    Dict,
    DictEntry,
    DictGroup,
    LocalePreset,
    OpenCCError,
    Trie,
    converter,
    converter_builder,
    converter_factory,
    converter_with_options,
    custom_converter,
)
from .html import HTMLConverter, HtmlConverter, html_converter

__all__ = [
    "Converter",
    "ConverterOptions",
    "Dict",
    "DictEntry",
    "DictGroup",
    "HTMLConverter",
    "HtmlConverter",
    "LocalePreset",
    "OpenCCError",
    "Trie",
    "converter",
    "converter_builder",
    "converter_factory",
    "converter_with_options",
    "custom_converter",
    "html_converter",
    "locale",
    "presets",
]
