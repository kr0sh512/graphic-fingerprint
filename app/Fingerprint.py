import re
import base64
import hashlib

from app import AUGMENTATION_STRING


class Fingerprint:
    __patterns = {
        "SHA1": r"(?:[0-9a-f]{2}:){19}[0-9a-f]{2} | [0-9a-f]{40}",
        "MD5": r"(?:[0-9A-Fa-f]{2}:){15}[0-9A-Fa-f]{2}|[0-9A-Fa-f]{32}",
        "SHA256": r"(?:SHA256:)?([A-Za-z0-9+/=]{20,})",
    }

    def __init__(self, fingerprint: str, ascii_art: str = None):
        self.fingerprint, self.type = self.__parse_fingerprint(fingerprint)
        self.ascii_art = (
            ascii_art if ascii_art else self.__generate_ascii_art(self.fingerprint)
        )

    def __parse_fingerprint(self, fingerprint):
        if isinstance(fingerprint, str):
            fingerprint = fingerprint.strip()

            for name, pattern in self.__patterns.items():
                matches = re.findall(pattern, fingerprint, flags=re.IGNORECASE)

                for match in matches:
                    # return match.replace(":", ""), name
                    if name == "SHA256":
                        return base64.b64decode(match), name

                    return bytes.fromhex(match.replace(":", "")), name

            raise ValueError("Invalid fingerprint format")
        else:
            raise TypeError("Fingerprint must be a string")

    def __generate_ascii_art(self, fingerprint, width=17, height=9):
        # symbols = " .o+=*BOX@%#"
        symbols = AUGMENTATION_STRING[:-2]
        grid = [[0 for _ in range(width)] for _ in range(height)]

        x, y = width // 2, height // 2  # Центр
        start_x, start_y = x, y

        for byte in fingerprint:
            for _ in range(2):
                nibble = byte & 0xF
                dx = (nibble & 1) - ((nibble >> 1) & 1)
                dy = ((nibble >> 2) & 1) - ((nibble >> 3) & 1)

                x = max(0, min(width - 1, x + dx))
                y = max(0, min(height - 1, y + dy))

                grid[y][x] += 1
                byte >>= 4

        result = []
        for j in range(height):
            line = ""
            for i in range(width):
                if (i, j) == (start_x, start_y):
                    line += "S"
                elif (i, j) == (x, y):
                    line += "E"
                else:
                    visits = grid[j][i]
                    visits = min(visits, len(symbols) - 1)
                    line += symbols[visits]
            result.append("|" + line + "|")

        # Add frame
        top_bottom = "+" + "-" * width + "+"
        return "\n".join([top_bottom] + result + [top_bottom])

    def __str__(self):
        return f"Fingerprint: {self.fingerprint.hex()}\nType\n{self.type}\nASCII Art:\n{self.ascii_art}"


def sha256():
    st = "SHA256:rFby2Z2Sl9ZRa69NLRs56zXOXE4PUkdlx+LxcbikwcY"
    pt = r"(?:SHA256:)?([A-Za-z0-9+/=]{20,})"

    matches = re.findall(pt, st, flags=re.IGNORECASE)
    print(matches)


if __name__ == "__main__":
    sha256()
    exit(0)

    st = "SHA256:rFby2Z2Sl9ZRa69NLRs56zXOXE4PUkdlx+LxcbikwcY"

    fin = Fingerprint(st)
    print(fin)
