from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass


class OpenCCError(ValueError):
    """Raised when a converter cannot be built from the requested options."""


@dataclass(frozen=True, slots=True)
class ConverterOptions:
    from_: str = ""
    to: str = ""


@dataclass(frozen=True, slots=True)
class DictEntry:
    source: str
    target: str


class Dict:
    def __init__(self, raw: str | None = None, entries: Iterable[DictEntry] | None = None) -> None:
        if raw is None and entries is None:
            raise ValueError("Either raw or entries must be provided.")
        if raw is not None and entries is not None:
            raise ValueError("Only one of raw or entries can be provided.")
        self._raw = raw
        self._entries = tuple(entries) if entries is not None else None

    @classmethod
    def from_string(cls, data: str) -> Dict:
        if data is None:
            raise TypeError("data cannot be None")
        return cls(raw=data)

    @classmethod
    def from_entries(cls, entries: Iterable[DictEntry | tuple[str, str]]) -> Dict:
        if entries is None:
            raise TypeError("entries cannot be None")
        if isinstance(entries, Mapping):
            entries = entries.items()
        converted = []
        for entry in entries:
            if isinstance(entry, DictEntry):
                converted.append(entry)
            else:
                source, target = entry
                converted.append(DictEntry(source, target))
        return cls(entries=converted)

    def load_into(self, trie: Trie) -> None:
        if self._raw is not None:
            trie.load_dict(self._raw)
        else:
            trie.load_entries(self._entries or ())


class DictGroup(Sequence[Dict]):
    def __init__(self, dicts: Iterable[Dict]) -> None:
        if dicts is None:
            raise TypeError("dicts cannot be None")
        self._dicts = tuple(dicts)

    @classmethod
    def from_strings(cls, *dicts: str) -> DictGroup:
        if dicts is None:
            raise TypeError("dicts cannot be None")
        return cls(Dict.from_string(data) for data in dicts)

    @classmethod
    def from_entries(cls, *dicts: Iterable[DictEntry | tuple[str, str]]) -> DictGroup:
        if dicts is None:
            raise TypeError("dicts cannot be None")
        return cls(Dict.from_entries(entries) for entries in dicts)

    def concat(self, dict_or_dicts: Dict | Iterable[Dict]) -> DictGroup:
        if isinstance(dict_or_dicts, Dict):
            return DictGroup((*self._dicts, dict_or_dicts))
        return DictGroup((*self._dicts, *tuple(dict_or_dicts)))

    def __getitem__(self, index: int) -> Dict:
        return self._dicts[index]

    def __len__(self) -> int:
        return len(self._dicts)


class _Node:
    __slots__ = ("children", "value")

    def __init__(self) -> None:
        self.children: dict[str, _Node] = {}
        self.value: str | None = None


class Trie:
    def __init__(self) -> None:
        self._root = _Node()

    def add_word(self, source: str, target: str) -> None:
        if source is None:
            raise TypeError("source cannot be None")
        if target is None:
            raise TypeError("target cannot be None")

        node = self._root
        for char in source:
            node = node.children.setdefault(char, _Node())
        node.value = target

    def load_dict(self, dict_data: str) -> None:
        if dict_data is None:
            raise TypeError("dict_data cannot be None")

        for line in dict_data.replace("|", "\n").split("\n"):
            line = line.strip()
            if not line:
                continue
            separator_index = line.find("\t")
            if separator_index < 0:
                separator_index = line.find(" ")
            if separator_index < 0:
                continue
            self.add_word(line[:separator_index], line[separator_index + 1 :])

    def load_entries(self, entries: Iterable[DictEntry | tuple[str, str]]) -> None:
        if entries is None:
            raise TypeError("entries cannot be None")
        for entry in entries:
            if isinstance(entry, DictEntry):
                self.add_word(entry.source, entry.target)
            else:
                source, target = entry
                self.add_word(source, target)

    def load_dict_like(self, dict_like: Dict) -> None:
        if dict_like is None:
            raise TypeError("dict_like cannot be None")
        dict_like.load_into(self)

    def load_dict_group(self, dicts: Iterable[Dict]) -> None:
        if dicts is None:
            raise TypeError("dicts cannot be None")
        for dict_like in dicts:
            self.load_dict_like(dict_like)

    def convert(self, input_text: str) -> str:
        if input_text is None:
            raise TypeError("input_text cannot be None")
        if input_text == "":
            return ""

        result: list[str] = []
        pending: list[str] = []
        i = 0
        length = len(input_text)

        while i < length:
            node = self._root
            matched_end = -1
            matched_value: str | None = None
            j = i

            while j < length:
                next_node = node.children.get(input_text[j])
                if next_node is None:
                    break
                j += 1
                node = next_node
                if node.value is not None:
                    matched_end = j
                    matched_value = node.value

            if matched_end >= 0:
                if pending:
                    result.append("".join(pending))
                    pending.clear()
                result.append(matched_value or "")
                i = matched_end
            else:
                pending.append(input_text[i])
                i += 1

        if pending:
            result.append("".join(pending))
        return "".join(result)


@dataclass(frozen=True, slots=True)
class LocalePreset:
    from_map: Mapping[str, DictGroup]
    to_map: Mapping[str, DictGroup]


class Converter:
    def __init__(self, dict_groups: Iterable[DictGroup]) -> None:
        if dict_groups is None:
            raise TypeError("dict_groups cannot be None")
        self._tries = []
        for group in dict_groups:
            if group is None:
                raise ValueError("Dictionary group cannot be None.")
            trie = Trie()
            trie.load_dict_group(group)
            self._tries.append(trie)

    def convert(self, input_text: str) -> str:
        if input_text is None:
            raise TypeError("input_text cannot be None")
        result = input_text
        for trie in self._tries:
            result = trie.convert(result)
        return result

    def __call__(self, input_text: str) -> str:
        return self.convert(input_text)


def converter(from_: str, to: str) -> Converter:
    return converter_with_options(ConverterOptions(from_, to))


def converter_with_options(options: ConverterOptions) -> Converter:
    from .locale_data import full_preset

    return converter_builder(full_preset())(options)


def converter_builder(locale_preset: LocalePreset) -> Callable[[ConverterOptions], Converter]:
    if locale_preset is None:
        raise TypeError("locale_preset cannot be None")

    def build(options: ConverterOptions) -> Converter:
        if options is None:
            raise TypeError("options cannot be None")
        dict_groups: list[DictGroup] = []
        _add_dict_group("from", options.from_, locale_preset.from_map, dict_groups)
        _add_dict_group("to", options.to, locale_preset.to_map, dict_groups)
        return converter_factory(*dict_groups)

    return build


def converter_factory(*dict_groups: DictGroup | Iterable[DictGroup]) -> Converter:
    if dict_groups is None:
        raise TypeError("dict_groups cannot be None")
    if len(dict_groups) == 1 and not isinstance(dict_groups[0], DictGroup):
        return Converter(dict_groups[0])
    return Converter(dict_groups)


def custom_converter(dict_data: str | Iterable[DictEntry | tuple[str, str]]) -> Converter:
    if dict_data is None:
        raise TypeError("dict_data cannot be None")
    if isinstance(dict_data, str):
        return converter_factory(DictGroup([Dict.from_string(dict_data)]))
    return converter_factory(DictGroup([Dict.from_entries(dict_data)]))


def _add_dict_group(
    kind: str,
    locale: str,
    mapping: Mapping[str, DictGroup],
    dict_groups: list[DictGroup],
) -> None:
    if locale is None or locale.strip() == "":
        raise OpenCCError(f"Please provide the `{kind}` option")
    if locale == "t":
        return
    try:
        group = mapping[locale]
    except KeyError as exc:
        raise OpenCCError(f"Unknown locale `{locale}` for `{kind}` option") from exc
    dict_groups.append(group)
