#!/usr/bin/env python3
"""Strip numeric tone marks (1-4) from pinyin tokens in a text file.

Usage:
  python scripts/strip_tones.py input.dict.yaml           # writes input-notone.dict.yaml
  python scripts/strip_tones.py -i input.dict.yaml       # inplace (with .bak backup)
  python scripts/strip_tones.py -o out.dict.yaml input.yaml

The script removes digits 1-4 that immediately follow ASCII letter sequences
used for pinyin (e.g., "jun1" -> "jun"). It preserves other digits (e.g. dates)
because those digits are not attached to letters.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path


def strip_tones(text: str) -> str:
    # Remove tone digits 1-4 that immediately follow ASCII letters.
    # Example: "jun1 zi3 hao3 qiu2" -> "jun zi hao qiu"
    # Use a conservative pattern: letters (a-zA-Z) followed by [1-4].
    return re.sub(r'(?P<p>[A-Za-z]+)[1-4]\b', lambda m: m.group('p'), text)


def process_file(src: Path, dst: Path, inplace: bool = False) -> Path:
    text = src.read_text(encoding='utf-8')
    new = strip_tones(text)
    if inplace:
        bak = src.with_suffix(src.suffix + '.bak')
        src.replace(bak)
        dst.write_text(new, encoding='utf-8')
        # restore name
        dst.replace(src)
        return src
    else:
        dst.write_text(new, encoding='utf-8')
        return dst


def main() -> None:
    p = argparse.ArgumentParser(description='Strip numeric pinyin tones (1-4) from a file.')
    p.add_argument('input', help='Input file path')
    p.add_argument('-o', '--output', help='Output file path (defaults to input-notone.ext)')
    p.add_argument('-i', '--inplace', action='store_true', help='Replace input file in-place (backup created with .bak)')
    args = p.parse_args()

    src = Path(args.input)
    if not src.exists():
        p.error(f'Input file does not exist: {src}')

    if args.inplace:
        # write to a temp path then move
        tmp = src.with_name(src.name + '.tmp')
        result = process_file(src, tmp, inplace=True)
        print(f'Updated in-place (backup at {src}.bak) -> {result}')
        return

    if args.output:
        dst = Path(args.output)
    else:
        # If the input filename contains '-terra.dict' in its name, replace that with '.dict'
        # (e.g., 'sjy-keng-kyim-qyim-khawq-terra.dict.yaml' -> 'sjy-keng-kyim-qyim-khawq.dict.yaml').
        name = src.name
        if '-terra.dict' in name:
            new_name = name.replace('-terra.dict', '.dict')
        else:
            # Fallback: append '-notone' to avoid overwriting the source when
            # there is no '-terra.dict' segment.
            stem = src.stem
            new_name = stem + '-notone' + src.suffix
        dst = src.with_name(new_name)

    result = process_file(src, dst, inplace=False)
    print(f'Wrote tone-free copy: {result}')


if __name__ == '__main__':
    main()
