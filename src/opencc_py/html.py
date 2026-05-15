from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
from xml.etree import ElementTree

from .core import Converter


class HtmlConverter:
    def __init__(
        self,
        converter: Converter | Callable[[str], str],
        root_node: ElementTree.Element | ElementTree.ElementTree,
        from_lang_tag: str,
        to_lang_tag: str,
    ) -> None:
        if converter is None:
            raise TypeError("converter cannot be None")
        if root_node is None:
            raise TypeError("root_node cannot be None")
        if from_lang_tag is None:
            raise TypeError("from_lang_tag cannot be None")
        if to_lang_tag is None:
            raise TypeError("to_lang_tag cannot be None")

        self._converter = converter.convert if isinstance(converter, Converter) else converter
        self._tree = root_node if isinstance(root_node, ElementTree.ElementTree) else None
        self._root = root_node.getroot() if isinstance(root_node, ElementTree.ElementTree) else root_node
        self._original = deepcopy(self._root)
        self._from_lang_tag = from_lang_tag
        self._to_lang_tag = to_lang_tag

    @classmethod
    def from_xml_string(
        cls,
        converter: Converter | Callable[[str], str],
        xml: str,
        from_lang_tag: str,
        to_lang_tag: str,
    ) -> HtmlConverter:
        return cls(converter, ElementTree.fromstring(xml), from_lang_tag, to_lang_tag)

    @property
    def root(self) -> ElementTree.Element:
        return self._root

    def convert(self) -> None:
        self._convert_element(self._root, False)

    def restore(self) -> None:
        self._root.clear()
        self._root.tag = self._original.tag
        self._root.attrib.update(self._original.attrib)
        self._root.text = self._original.text
        self._root.tail = self._original.tail
        self._root.extend(deepcopy(list(self._original)))
        if self._tree is not None:
            self._tree._setroot(self._root)

    def to_xml_string(self, encoding: str = "unicode") -> str:
        return ElementTree.tostring(self._root, encoding=encoding)  # type: ignore[return-value]

    def _convert_element(self, element: ElementTree.Element, lang_matched: bool) -> None:
        if _has_ignore_class(element):
            return

        lang = element.attrib.get("lang")
        if lang == self._from_lang_tag:
            lang_matched = True
            element.attrib["lang"] = self._to_lang_tag
        elif lang:
            lang_matched = False

        tag_name = _local_name(element.tag)
        if lang_matched and tag_name in {"script", "style"}:
            return

        if lang_matched:
            self._convert_special_attributes(element, tag_name)
            if element.text is not None:
                element.text = self._converter(element.text)

        for child in list(element):
            self._convert_element(child, lang_matched)
            if lang_matched and child.tail is not None:
                child.tail = self._converter(child.tail)

    def _convert_special_attributes(self, element: ElementTree.Element, tag_name: str) -> None:
        if tag_name == "meta" and element.attrib.get("name", "").lower() in {"description", "keywords"}:
            if "content" in element.attrib:
                element.attrib["content"] = self._converter(element.attrib["content"])
        elif tag_name == "img":
            if "alt" in element.attrib:
                element.attrib["alt"] = self._converter(element.attrib["alt"])
        elif tag_name == "input" and element.attrib.get("type", "").lower() == "button":
            if "value" in element.attrib:
                element.attrib["value"] = self._converter(element.attrib["value"])


HTMLConverter = HtmlConverter


def html_converter(
    converter: Converter | Callable[[str], str],
    root_node: ElementTree.Element | ElementTree.ElementTree,
    from_lang_tag: str,
    to_lang_tag: str,
) -> HtmlConverter:
    return HtmlConverter(converter, root_node, from_lang_tag, to_lang_tag)


def _has_ignore_class(element: ElementTree.Element) -> bool:
    return "ignore-opencc" in element.attrib.get("class", "").split()


def _local_name(tag: str) -> str:
    if "}" in tag:
        tag = tag.rsplit("}", 1)[1]
    return tag.lower()
