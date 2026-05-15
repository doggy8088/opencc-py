from __future__ import annotations

from .core import DictGroup
from .locale_data import (
    from_cn,
    from_hk,
    from_jp,
    from_map,
    from_tw,
    from_tw2,
    from_twp,
    to_cn,
    to_hk,
    to_jp,
    to_map,
    to_tw,
    to_tw2,
    to_twp,
)


class From:
    cn = staticmethod(from_cn)
    hk = staticmethod(from_hk)
    tw = staticmethod(from_tw)
    tw2 = staticmethod(from_tw2)
    twp = staticmethod(from_twp)
    jp = staticmethod(from_jp)


class To:
    cn = staticmethod(to_cn)
    hk = staticmethod(to_hk)
    tw = staticmethod(to_tw)
    tw2 = staticmethod(to_tw2)
    twp = staticmethod(to_twp)
    jp = staticmethod(to_jp)


def get_from(locale: str) -> DictGroup:
    return from_map()[locale]


def get_to(locale: str) -> DictGroup:
    return to_map()[locale]


__all__ = ["From", "To", "from_map", "get_from", "get_to", "to_map"]
