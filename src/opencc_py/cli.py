from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .core import OpenCCError, converter


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="opencc-py",
        description="Convert Chinese text between OpenCC locales.",
    )
    parser.add_argument("file", help="Input UTF-8 text file")
    parser.add_argument("from_locale", help="Source locale: cn, hk, tw, tw2, twp, jp, or t")
    parser.add_argument("to_locale", help="Target locale: cn, hk, tw, tw2, twp, jp, or t")
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument("-o", "--output", help="Output file path")
    output_group.add_argument("-i", "--in-place", action="store_true", help="Overwrite the input file")

    args = parser.parse_args(argv)

    try:
        input_path = Path(args.file)
        content = input_path.read_text(encoding="utf-8")
        converted = converter(args.from_locale, args.to_locale).convert(content)

        if args.output:
            Path(args.output).write_text(converted, encoding="utf-8")
        elif args.in_place:
            input_path.write_text(converted, encoding="utf-8")
        else:
            sys.stdout.write(converted)
            if converted and not converted.endswith("\n"):
                sys.stdout.write("\n")
    except (OSError, OpenCCError, UnicodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
