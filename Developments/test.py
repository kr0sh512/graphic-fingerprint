import subprocess
import sys
from colorama import init, Fore, Style

from enum import Enum

init()

proc = subprocess.Popen(
    ["ssh-keygen"] + sys.argv[1:],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)


class Status(Enum):
    ENTER = 1
    GENERATING = 2
    ERROR = 3
    OTHER = 4


status = Status.ENTER

out = ""


def colorize_output(char):
    if "+" not in out:
        return char

    # if out.count("+") == 1:
    #     print("\033[H\033[J", end="")

    match char:
        case ".":
            return Fore.RED + char + Style.RESET_ALL  # Red
        case "+":
            return Fore.GREEN + char + Style.RESET_ALL  # Green
        case "=":
            return Fore.YELLOW + char + Style.RESET_ALL  # Yellow
        case "E":
            return Fore.BLUE + char + Style.RESET_ALL  # Blue
        case "B":
            return Fore.BLUE + char + Style.RESET_ALL  # Blue
        case "O":
            return Fore.BLUE + char + Style.RESET_ALL  # Blue
        case "o":
            return Fore.BLUE + char + Style.RESET_ALL  # Blue
        case _:
            return char


while True:
    char = proc.stdout.read(1)
    if not char:
        break

    if char == "\n":
        if status == Status.ENTER:
            status = Status.GENERATING
        elif status == Status.GENERATING:
            status = Status.ERROR
        elif status == Status.ERROR:
            status = Status.OTHER

    out += char

    sys.stdout.write(colorize_output(char))
    sys.stdout.flush()

    # sys.stdout.write(char.decode("utf-8", errors="replace"))
    # sys.stdout.flush()


# for line in proc.stdout:
#     # Красим разные строки по смыслу
#     if "Enter" in line or "Введите" in line:
#         print(Fore.YELLOW + line.rstrip() + Style.RESET_ALL)
#     elif "Generating" in line or "создание" in line:
#         print(Fore.CYAN + line.rstrip() + Style.RESET_ALL)
#     elif "error" in line.lower() or "ошибка" in line.lower():
#         print(Fore.RED + line.rstrip() + Style.RESET_ALL)
#     else:
#         print(line.rstrip())

proc.wait()
