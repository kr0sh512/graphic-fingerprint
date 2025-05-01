import colorama
import random

from app import AUGMENTATION_STRING


class Colorize:
    def __init__(self, fingerprint):
        self.fingerprint = fingerprint
        self.colorama = colorama
        self.colorama.init(autoreset=True)
        self.colors = {
            "red": self.colorama.Fore.RED,
            "green": self.colorama.Fore.GREEN,
            "yellow": self.colorama.Fore.YELLOW,
            "blue": self.colorama.Fore.BLUE,
            "magenta": self.colorama.Fore.MAGENTA,
            "cyan": self.colorama.Fore.CYAN,
            "white": self.colorama.Fore.WHITE,
            "reset": self.colorama.Style.RESET_ALL,
        }
        self.colorized_map = self.__create_color_map()

    def __create_color_map(self):
        color_map = {}
        for char in AUGMENTATION_STRING[1:-2]:
            random.seed(ord(char) + self.fingerprint)
            color_map[char] = random.choice(list(self.colors.values()))

        return color_map

    def colorize(self, char):
        if char in self.colorized_map:
            return self.colorized_map[char] + char + self.colors["reset"]
        else:
            return char

    def __colorize_frame(self, text):
        pass

    def colorize_fingerprint(self, text, has_frame=False):
        str_list = text.split("\n")
        frame = None
        if has_frame:
            frame = [str_list[0], str_list[-1]]
            str_list = str_list[1:-1]
            str_list = [st.replace("|", "") for st in str_list]
        text = "\n".join(str_list)

        # change text on class Key
        colorized_fingerprint = ""

        for char in text:
            colorized_fingerprint += self.colorize(char)

        if has_frame:
            colorized_fingerprint = "\n".join(
                [f"|{st}|" for st in colorized_fingerprint.split("\n")]
            )
            colorized_fingerprint = (
                frame[0] + "\n" + colorized_fingerprint + "\n" + frame[1]
            )

        return colorized_fingerprint
