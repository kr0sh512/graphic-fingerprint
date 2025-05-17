import random
import re
import os
from math import log2, ceil, factorial

from Fingerprint import Fingerprint

WORDS_NUM = 4
EMOJI_NUM = WORDS_NUM * 2

WORDS_PATH = "files/words.txt"
EMOJI_PATH = "files/emoji.md"

TEST_MD5 = "15:b9:af:f6:9d:41:16:bc:39:35:ef:9c:e4:da:9f:b7"
TEST2_MD5 = "04:e8:74:67:c0:9f:bb:c5:c7:b6:68:a9:48:1d:8d:f2"

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def parse_emoji(path: str) -> list[str]:
    emojis = []
    pattern = r"(.+) \| `(:[^`]+:)` \| (.+)"

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(pattern, line, re.UNICODE)

            if (
                match
                and (len(match.group(1)) == 1)
                # and ("ZERO WIDTH" not in match.group(3))
            ):

                emojis.append(match.group(1))

    return emojis


def parse_words(path: str, with_upper: bool = True) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        words = [word[:-1].lower() for word in f]

        if with_upper:
            words.extend([word.upper() for word in words])

        return words


def num_from_bits(data: list[int]) -> int:
    num = 0

    for i in range(len(data)):
        num += data[i] << i

    return num


def print_result(emoji: list[str], words: list[str]) -> None:
    for i in range(WORDS_NUM):
        print(f"{emoji[i]} - {words[i]} - {emoji[i + 4]}")


if __name__ == "__main__":
    list_emoji = parse_emoji(EMOJI_PATH)[:250]
    list_words = parse_words(WORDS_PATH)

    fp = Fingerprint(TEST_MD5)
    print(fp.str_fp)

    data = fp.fingerprint
    bit_array = [(data[int(i // 8)] >> int(i % 8)) & 0x1 for i in range(len(data) * 8)]

    random.seed(fp.fingerprint)
    random.shuffle(bit_array)
    random.shuffle(list_words)
    random.shuffle(list_emoji)

    for_word = ceil(log2(len(list_words)))  # 15
    for_emoji = ceil(log2(len(list_emoji)))  # 8

    for_words_shuffle = ceil(log2(factorial(WORDS_NUM)))  # 5
    for_emoji_shuffle = ceil(log2(factorial(EMOJI_NUM)))  # 16

    # print(
    #     f"for_word: {for_word * WORDS_NUM}, \
    #       \tfor_emoji: {for_emoji * EMOJI_NUM}"
    # )  # 60 and 64

    fp_emoji = [
        list_emoji[i % len(list_emoji)]
        for i in [
            num_from_bits(bit_array[i * for_emoji : (i + 1) * for_emoji])
            for i in range(EMOJI_NUM)
        ]
    ]

    fp_words = [
        list_words[i % len(list_words)]
        for i in [
            num_from_bits(
                bit_array[for_emoji * EMOJI_NUM :][i * for_word : (i + 1) * for_word]
            )
            for i in range(WORDS_NUM)
        ]
    ]

    for i in range(WORDS_NUM):
        print(f"{fp_emoji[i]} - {fp_words[i]} - {fp_emoji[i + 4]}")

    exit(0)
