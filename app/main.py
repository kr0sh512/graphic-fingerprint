#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import sys
from colorama import Fore, Style, Back, init

init(autoreset=True)


def test():
    import Fingerprint

    # fp = Fingerprint.Fingerprint("A0:1B:2C:3D:4E:5F:6A:7B:8C:9D:0E:1F:2A:3B:4C:5D")
    fp = Fingerprint.Fingerprint("SHA256:rFby2Z2Sl9ZRa69NLRs56zXOXE4PUkdlx+LxcbikwcY")

    print(fp)

    import Colorize

    Color = Colorize.Colorize(0)

    text = """\
+---[RSA 3072]----+
|           o   o+|
|            E =o=|
|           . = ==|
|       .    . ooo|
|      . S     oo.|
|       = o o =.+o|
|      o o + B B.B|
|     .     + .+#+|
|             .=++|
+----[SHA256]-----+\
"""

    print(Color.colorize_fingerprint(text, has_frame=True))

    print("Test")
    print(Fore.RED + "This is red text")
    print(Back.GREEN + "This is green background")
    print(Style.BRIGHT + "This is bright text")
    print(Style.RESET_ALL + "This is normal text")
    print(Fore.RED + "Это красный текст")
    print(Fore.WHITE + Back.GREEN + Fore.WHITE + "А это текст на зелёном фоне")
    print(Style.BRIGHT + "Яркий стиль текста")

    return


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1]:
        test()
        exit(0)

    proc = subprocess.Popen(
        ["ssh-keygen"] + sys.argv[1:],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    while True:
        char = proc.stdout.read(1)
        if not char:
            break

        sys.stdout.write(char)
        sys.stdout.flush()

    proc.wait()
    sys.stdout.write("\n")
    sys.stdout.flush()
