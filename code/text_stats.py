"""统计文本中的英文单词词频。

用法：
    python code/text_stats.py <文本文件路径>
    Get-Content <文本文件路径> | python code/text_stats.py
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


def count_words(text: str) -> Counter[str]:
    """返回文本中不区分大小写的英文单词词频。"""
    words = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text.lower())
    return Counter(words)


def main() -> None:
    parser = argparse.ArgumentParser(description="统计文本中的英文单词词频")
    parser.add_argument("file", nargs="?", type=Path, help="要统计的 UTF-8 文本文件")
    parser.add_argument("-n", "--top", type=int, default=10, help="显示词频最高的前 N 个词（默认：10）")
    args = parser.parse_args()

    if args.top < 1:
        parser.error("--top 必须是正整数")

    if args.file:
        try:
            text = args.file.read_text(encoding="utf-8")
        except OSError as error:
            parser.error(f"无法读取文件：{error}")
    else:
        text = sys.stdin.read()

    counts = count_words(text)
    print(f"总词数：{sum(counts.values())}")
    print(f"不同词数：{len(counts)}")
    print("词频最高的词：")
    for word, frequency in counts.most_common(args.top):
        print(f"{word}: {frequency}")


if __name__ == "__main__":
    main()
