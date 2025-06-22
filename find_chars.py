import json
import re

with open("dataset/clean/text_data.json", "r") as file:
    data = json.load(file)


pattern = re.compile(
    r"(\\u[0-9a-fA-F]{4})|[\ue000-\uf8ff]|([^\x00-\x7FążźćńółęśĄŻŹĆŃÓŁĘŚ])"
)

glyphs_to_code = {
    "\u0105": "ą",
    "\u0119": "ę",
    "\u01f3": "n",
    "\ueeca": "f",
    "\u0133": "j",
    "\u013a": "ĺ",
    "\u01c9": "lj",
    "\u01f1": "Ę",
    "\u01f2": "Dz",
    "\u24b2": "(w)",
    "\ufb00": "ff",
    "\ufb01": "fi",
    "\ufb02": "fl",
    "\u0c17": "j",
    # Polish big
    "\u0c1a": "Ą",
    "\u0c1b": "Ć",
    "\u0c1c": "Ę",
    "\u0c1d": "Ł",
    "\u0c1e": "Ń",
    "\u0c1f": "Ś",
    "\u0c20": "Ź",
    "\u0c21": "Ż",
    "\u1f00": "ἀ",
    # Special
    "\u2013": "-",
    "\u2014": "-",
    "\u201e": '"',
    "\u201d": '"',
    "\u2019": "'",
    "\u2025": "..",
    "\u2026": "...",
    "\u203c": "!!",
    # Numeric
    "\u2070": "0",
    "\u2071": "1",
    "\u2072": "2",
    "\u2073": "3",
    "\u2074": "4",
    "\u2075": "5",
    "\u2076": "6",
    "\u2077": "7",
    "\u2078": "8",
    "\u2079": "9",
    "\uf730": "0",
    "\uf731": "1",
    "\uf732": "2",
    "\uf733": "3",
    "\uf734": "4",
    "\uf735": "5",
    "\uf736": "6",
    "\uf737": "7",
    "\uf738": "8",
    "\uf739": "9",
    # Cyrylic
    "\u041a": "K",
    "\u041f": "П",
    "\u0420": "P",
    "\u0430": "a",
    "\u0432": "B",
    "\u0438": "и",
    "\u043c": "M",
    "\u043b": "л",
    "\u043e": "o",
    "\u043d": "H",
    "\u0441": "c",
    "\u0442": "T",
    "\u0447": "ч",
    # Greek
    "\u03c2": "ς",
    "\u03ac": "ά",
    "\u03c3": "σ",
    "\u03c9": "ω",
    "\u03b3": "γ",
    "\u03bd": "v",
    "\u03b9": "ι",
    # Escape chars
    "\uf761": "",
    "\uf763": "",
    "\uf764": "",
    "\uf765": "",
    "\uf769": "",
    "\uf76a": "",
    "\uf76b": "",
    "\uf76d": "",
    "\uf774": "",
    "\uf777": "",
    "\uf77a": "",
    "\xe1": "",
    "\xb3": "",
    "\xab": "",
    "\xe2": "",
    "\xf4": "",
    "\xea": "",
    "\xe4": "",
    "\xbb": "",
    "\xe8": "",
    "\xf6": "",
    "\xb2": "",
    "\xe9": "",
    "\xfc": "",
    "\xb9": "",
    "\xe7": "",
    "\xe0": "",
}


unique_chars: set[str] = set()
for i in range(len(data)):
    text = data[i]["text"]

    for glyph, unicode_char in glyphs_to_code.items():
        text = text.replace(glyph, unicode_char)

    matches: list[str] = []
    for match in pattern.finditer(text):
        groups = match.groups()
        for m in groups:
            if m is not None:
                matches.append(m)

    for char in matches:
        unique_chars.add(f"{char}: {char.encode('unicode_escape').decode('ascii')}")

for char in unique_chars:
    print(char)
